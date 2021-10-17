/*

Faster and better CRISPR guide RNA design with the Crackling method.
Jacob Bradford, Timothy Chappell, Dimitri Perrin
bioRxiv 2020.02.14.950261; doi: https://doi.org/10.1101/2020.02.14.950261


To compile:

g++ -o isslScoreOfftargets isslScoreOfftargets.cpp -O3 -std=c++11 -fopenmp -mpopcnt -Iparallel_hashmap

*/


#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>
#include <chrono>
#include <bitset>
#include <iostream>
#include <climits>
#include <stdio.h>
#include <cstring>
#include <omp.h>
#include <phmap.h>
#include <map>

using namespace std;

size_t seqLength, seqCount, sliceWidth, sliceCount, offtargetsCount, scoresCount;

vector<uint8_t> nucleotideIndex(256);
vector<char> signatureIndex(4);

size_t getFileSize(const char *path)
{
    struct stat64 statBuf;
    stat64(path, &statBuf);
    return statBuf.st_size;
}

uint64_t sequenceToSignature(const char *ptr)
{
    uint64_t signature = 0;
    for (size_t j = 0; j < seqLength; j++) {
        signature |= (uint64_t)(nucleotideIndex[*ptr]) << (j * 2);
        ptr++;
    }
    return signature;
}

string signatureToSequence(uint64_t signature)
{
    string sequence = string(seqLength, ' ');
    for (size_t j = 0; j < seqLength; j++) {
        sequence[j] = signatureIndex[(signature >> (j * 2)) & 0x3];
    }
    return sequence;
}

int main(int argc, char **argv)
{
    if (argc < 3) {
        fprintf(stderr, "Usage: %s [issltable] [query file] [max distance] [score-threshold]\n", argv[0]);
        exit(1);
    }
    
    nucleotideIndex['A'] = 0;
    nucleotideIndex['C'] = 1;
    nucleotideIndex['G'] = 2;
    nucleotideIndex['T'] = 3;
    signatureIndex[0] = 'A';
    signatureIndex[1] = 'C';
    signatureIndex[2] = 'G';
    signatureIndex[3] = 'T';
    
	double cfdPosPenalties[320] = {
		// mask = pos << 4
		// mask |= guide[pos] << 2
		// mask |= revcom(offtarget[pos])
		// 0: A, 1: C, 2: G, 3: T
		
		1.0000000000, // (  0) 0:A-A 0b000000000
		1.0000000000, // (  1) 0:C-C 0b000000001
		0.8571428570, // (  2) 0:G-G 0b000000010
		1.0000000000, // (  3) 0:T-T 0b000000011
		1.0000000000, // (  4) 0:A-A 0b000000100
		0.9130434780, // (  5) 0:C-C 0b000000101
		1.0000000000, // (  6) 0:G-G 0b000000110
		1.0000000000, // (  7) 0:T-T 0b000000111
		1.0000000000, // (  8) 0:A-A 0b000001000
		1.0000000000, // (  9) 0:C-C 0b000001001
		0.7142857140, // ( 10) 0:G-G 0b000001010
		0.9000000000, // ( 11) 0:T-T 0b000001011
		1.0000000000, // ( 12) 0:A-A 0b000001100
		0.9565217390, // ( 13) 0:C-C 0b000001101
		0.8571428570, // ( 14) 0:G-G 0b000001110
		1.0000000000, // ( 15) 0:T-T 0b000001111
		0.7272727270, // ( 16) 1:A-A 0b000010000
		0.8000000000, // ( 17) 1:C-C 0b000010001
		0.7857142860, // ( 18) 1:G-G 0b000010010
		1.0000000000, // ( 19) 1:T-T 0b000010011
		0.9090909090, // ( 20) 1:A-A 0b000010100
		0.6956521740, // ( 21) 1:C-C 0b000010101
		1.0000000000, // ( 22) 1:G-G 0b000010110
		0.7272727270, // ( 23) 1:T-T 0b000010111
		0.6363636360, // ( 24) 1:A-A 0b000011000
		1.0000000000, // ( 25) 1:C-C 0b000011001
		0.6923076920, // ( 26) 1:G-G 0b000011010
		0.8461538460, // ( 27) 1:T-T 0b000011011
		1.0000000000, // ( 28) 1:A-A 0b000011100
		0.8400000000, // ( 29) 1:C-C 0b000011101
		0.8571428570, // ( 30) 1:G-G 0b000011110
		0.8461538460, // ( 31) 1:T-T 0b000011111
		0.7058823530, // ( 32) 2:A-A 0b000100000
		0.6111111110, // ( 33) 2:C-C 0b000100001
		0.4285714290, // ( 34) 2:G-G 0b000100010
		1.0000000000, // ( 35) 2:T-T 0b000100011
		0.6875000000, // ( 36) 2:A-A 0b000100100
		0.5000000000, // ( 37) 2:C-C 0b000100101
		1.0000000000, // ( 38) 2:G-G 0b000100110
		0.8666666670, // ( 39) 2:T-T 0b000100111
		0.5000000000, // ( 40) 2:A-A 0b000101000
		1.0000000000, // ( 41) 2:C-C 0b000101001
		0.3846153850, // ( 42) 2:G-G 0b000101010
		0.7500000000, // ( 43) 2:T-T 0b000101011
		1.0000000000, // ( 44) 2:A-A 0b000101100
		0.5000000000, // ( 45) 2:C-C 0b000101101
		0.4285714290, // ( 46) 2:G-G 0b000101110
		0.7142857140, // ( 47) 2:T-T 0b000101111
		0.6363636360, // ( 48) 3:A-A 0b000110000
		0.6250000000, // ( 49) 3:C-C 0b000110001
		0.3529411760, // ( 50) 3:G-G 0b000110010
		1.0000000000, // ( 51) 3:T-T 0b000110011
		0.8000000000, // ( 52) 3:A-A 0b000110100
		0.5000000000, // ( 53) 3:C-C 0b000110101
		1.0000000000, // ( 54) 3:G-G 0b000110110
		0.8421052630, // ( 55) 3:T-T 0b000110111
		0.3636363640, // ( 56) 3:A-A 0b000111000
		1.0000000000, // ( 57) 3:C-C 0b000111001
		0.5294117650, // ( 58) 3:G-G 0b000111010
		0.9000000000, // ( 59) 3:T-T 0b000111011
		1.0000000000, // ( 60) 3:A-A 0b000111100
		0.6250000000, // ( 61) 3:C-C 0b000111101
		0.6470588240, // ( 62) 3:G-G 0b000111110
		0.4761904760, // ( 63) 3:T-T 0b000111111
		0.3636363640, // ( 64) 4:A-A 0b001000000
		0.7200000000, // ( 65) 4:C-C 0b001000001
		0.5000000000, // ( 66) 4:G-G 0b001000010
		1.0000000000, // ( 67) 4:T-T 0b001000011
		0.6363636360, // ( 68) 4:A-A 0b001000100
		0.6000000000, // ( 69) 4:C-C 0b001000101
		1.0000000000, // ( 70) 4:G-G 0b001000110
		0.5714285710, // ( 71) 4:T-T 0b001000111
		0.3000000000, // ( 72) 4:A-A 0b001001000
		1.0000000000, // ( 73) 4:C-C 0b001001001
		0.7857142860, // ( 74) 4:G-G 0b001001010
		0.8666666670, // ( 75) 4:T-T 0b001001011
		1.0000000000, // ( 76) 4:A-A 0b001001100
		0.6400000000, // ( 77) 4:C-C 0b001001101
		1.0000000000, // ( 78) 4:G-G 0b001001110
		0.5000000000, // ( 79) 4:T-T 0b001001111
		0.7142857140, // ( 80) 5:A-A 0b001010000
		0.7142857140, // ( 81) 5:C-C 0b001010001
		0.4545454550, // ( 82) 5:G-G 0b001010010
		1.0000000000, // ( 83) 5:T-T 0b001010011
		0.9285714290, // ( 84) 5:A-A 0b001010100
		0.5000000000, // ( 85) 5:C-C 0b001010101
		1.0000000000, // ( 86) 5:G-G 0b001010110
		0.9285714290, // ( 87) 5:T-T 0b001010111
		0.6666666670, // ( 88) 5:A-A 0b001011000
		1.0000000000, // ( 89) 5:C-C 0b001011001
		0.6818181820, // ( 90) 5:G-G 0b001011010
		1.0000000000, // ( 91) 5:T-T 0b001011011
		1.0000000000, // ( 92) 5:A-A 0b001011100
		0.5714285710, // ( 93) 5:C-C 0b001011101
		0.9090909090, // ( 94) 5:G-G 0b001011110
		0.8666666670, // ( 95) 5:T-T 0b001011111
		0.4375000000, // ( 96) 6:A-A 0b001100000
		0.7058823530, // ( 97) 6:C-C 0b001100001
		0.4375000000, // ( 98) 6:G-G 0b001100010
		1.0000000000, // ( 99) 6:T-T 0b001100011
		0.8125000000, // (100) 6:A-A 0b001100100
		0.4705882350, // (101) 6:C-C 0b001100101
		1.0000000000, // (102) 6:G-G 0b001100110
		0.7500000000, // (103) 6:T-T 0b001100111
		0.5714285710, // (104) 6:A-A 0b001101000
		1.0000000000, // (105) 6:C-C 0b001101001
		0.6875000000, // (106) 6:G-G 0b001101010
		1.0000000000, // (107) 6:T-T 0b001101011
		1.0000000000, // (108) 6:A-A 0b001101100
		0.5882352940, // (109) 6:C-C 0b001101101
		0.6875000000, // (110) 6:G-G 0b001101110
		0.8750000000, // (111) 6:T-T 0b001101111
		0.4285714290, // (112) 7:A-A 0b001110000
		0.7333333330, // (113) 7:C-C 0b001110001
		0.4285714290, // (114) 7:G-G 0b001110010
		1.0000000000, // (115) 7:T-T 0b001110011
		0.8750000000, // (116) 7:A-A 0b001110100
		0.6428571430, // (117) 7:C-C 0b001110101
		1.0000000000, // (118) 7:G-G 0b001110110
		0.6500000000, // (119) 7:T-T 0b001110111
		0.6250000000, // (120) 7:A-A 0b001111000
		1.0000000000, // (121) 7:C-C 0b001111001
		0.6153846150, // (122) 7:G-G 0b001111010
		1.0000000000, // (123) 7:T-T 0b001111011
		1.0000000000, // (124) 7:A-A 0b001111100
		0.7333333330, // (125) 7:C-C 0b001111101
		1.0000000000, // (126) 7:G-G 0b001111110
		0.8000000000, // (127) 7:T-T 0b001111111
		0.6000000000, // (128) 8:A-A 0b010000000
		0.6666666670, // (129) 8:C-C 0b010000001
		0.5714285710, // (130) 8:G-G 0b010000010
		1.0000000000, // (131) 8:T-T 0b010000011
		0.8750000000, // (132) 8:A-A 0b010000100
		0.6190476190, // (133) 8:C-C 0b010000101
		1.0000000000, // (134) 8:G-G 0b010000110
		0.8571428570, // (135) 8:T-T 0b010000111
		0.5333333330, // (136) 8:A-A 0b010001000
		1.0000000000, // (137) 8:C-C 0b010001001
		0.5384615380, // (138) 8:G-G 0b010001010
		0.6428571430, // (139) 8:T-T 0b010001011
		1.0000000000, // (140) 8:A-A 0b010001100
		0.6190476190, // (141) 8:C-C 0b010001101
		0.9230769230, // (142) 8:G-G 0b010001110
		0.9285714290, // (143) 8:T-T 0b010001111
		0.8823529410, // (144) 9:A-A 0b010010000
		0.5555555560, // (145) 9:C-C 0b010010001
		0.3333333330, // (146) 9:G-G 0b010010010
		1.0000000000, // (147) 9:T-T 0b010010011
		0.9411764710, // (148) 9:A-A 0b010010100
		0.3888888890, // (149) 9:C-C 0b010010101
		1.0000000000, // (150) 9:G-G 0b010010110
		0.8666666670, // (151) 9:T-T 0b010010111
		0.8125000000, // (152) 9:A-A 0b010011000
		1.0000000000, // (153) 9:C-C 0b010011001
		0.4000000000, // (154) 9:G-G 0b010011010
		0.9333333330, // (155) 9:T-T 0b010011011
		1.0000000000, // (156) 9:A-A 0b010011100
		0.5000000000, // (157) 9:C-C 0b010011101
		0.5333333330, // (158) 9:G-G 0b010011110
		0.8571428570, // (159) 9:T-T 0b010011111
		0.3076923080, // (160) 10:A-A 0b010100000
		0.6500000000, // (161) 10:C-C 0b010100001
		0.4000000000, // (162) 10:G-G 0b010100010
		1.0000000000, // (163) 10:T-T 0b010100011
		0.3076923080, // (164) 10:A-A 0b010100100
		0.2500000000, // (165) 10:C-C 0b010100101
		1.0000000000, // (166) 10:G-G 0b010100110
		0.7500000000, // (167) 10:T-T 0b010100111
		0.3846153850, // (168) 10:A-A 0b010101000
		1.0000000000, // (169) 10:C-C 0b010101001
		0.4285714290, // (170) 10:G-G 0b010101010
		1.0000000000, // (171) 10:T-T 0b010101011
		1.0000000000, // (172) 10:A-A 0b010101100
		0.4000000000, // (173) 10:C-C 0b010101101
		0.6666666670, // (174) 10:G-G 0b010101110
		0.7500000000, // (175) 10:T-T 0b010101111
		0.3333333330, // (176) 11:A-A 0b010110000
		0.7222222220, // (177) 11:C-C 0b010110001
		0.2631578950, // (178) 11:G-G 0b010110010
		1.0000000000, // (179) 11:T-T 0b010110011
		0.5384615380, // (180) 11:A-A 0b010110100
		0.4444444440, // (181) 11:C-C 0b010110101
		1.0000000000, // (182) 11:G-G 0b010110110
		0.7142857140, // (183) 11:T-T 0b010110111
		0.3846153850, // (184) 11:A-A 0b010111000
		1.0000000000, // (185) 11:C-C 0b010111001
		0.5294117650, // (186) 11:G-G 0b010111010
		0.9333333330, // (187) 11:T-T 0b010111011
		1.0000000000, // (188) 11:A-A 0b010111100
		0.5000000000, // (189) 11:C-C 0b010111101
		0.9473684210, // (190) 11:G-G 0b010111110
		0.8000000000, // (191) 11:T-T 0b010111111
		0.3000000000, // (192) 12:A-A 0b011000000
		0.6521739130, // (193) 12:C-C 0b011000001
		0.2105263160, // (194) 12:G-G 0b011000010
		1.0000000000, // (195) 12:T-T 0b011000011
		0.7000000000, // (196) 12:A-A 0b011000100
		0.1363636360, // (197) 12:C-C 0b011000101
		1.0000000000, // (198) 12:G-G 0b011000110
		0.3846153850, // (199) 12:T-T 0b011000111
		0.3000000000, // (200) 12:A-A 0b011001000
		1.0000000000, // (201) 12:C-C 0b011001001
		0.4210526320, // (202) 12:G-G 0b011001010
		0.9230769230, // (203) 12:T-T 0b011001011
		1.0000000000, // (204) 12:A-A 0b011001100
		0.2608695650, // (205) 12:C-C 0b011001101
		0.7894736840, // (206) 12:G-G 0b011001110
		0.6923076920, // (207) 12:T-T 0b011001111
		0.5333333330, // (208) 13:A-A 0b011010000
		0.4666666670, // (209) 13:C-C 0b011010001
		0.2142857140, // (210) 13:G-G 0b011010010
		1.0000000000, // (211) 13:T-T 0b011010011
		0.7333333330, // (212) 13:A-A 0b011010100
		0.0000000000, // (213) 13:C-C 0b011010101
		1.0000000000, // (214) 13:G-G 0b011010110
		0.3500000000, // (215) 13:T-T 0b011010111
		0.2666666670, // (216) 13:A-A 0b011011000
		1.0000000000, // (217) 13:C-C 0b011011001
		0.4285714290, // (218) 13:G-G 0b011011010
		0.7500000000, // (219) 13:T-T 0b011011011
		1.0000000000, // (220) 13:A-A 0b011011100
		0.0000000000, // (221) 13:C-C 0b011011101
		0.2857142860, // (222) 13:G-G 0b011011110
		0.6190476190, // (223) 13:T-T 0b011011111
		0.2000000000, // (224) 14:A-A 0b011100000
		0.6500000000, // (225) 14:C-C 0b011100001
		0.2727272730, // (226) 14:G-G 0b011100010
		1.0000000000, // (227) 14:T-T 0b011100011
		0.0666666670, // (228) 14:A-A 0b011100100
		0.0500000000, // (229) 14:C-C 0b011100101
		1.0000000000, // (230) 14:G-G 0b011100110
		0.2222222220, // (231) 14:T-T 0b011100111
		0.1428571430, // (232) 14:A-A 0b011101000
		1.0000000000, // (233) 14:C-C 0b011101001
		0.2727272730, // (234) 14:G-G 0b011101010
		0.9411764710, // (235) 14:T-T 0b011101011
		1.0000000000, // (236) 14:A-A 0b011101100
		0.0500000000, // (237) 14:C-C 0b011101101
		0.2727272730, // (238) 14:G-G 0b011101110
		0.5789473680, // (239) 14:T-T 0b011101111
		0.0000000000, // (240) 15:A-A 0b011110000
		0.1923076920, // (241) 15:C-C 0b011110001
		0.0000000000, // (242) 15:G-G 0b011110010
		1.0000000000, // (243) 15:T-T 0b011110011
		0.3076923080, // (244) 15:A-A 0b011110100
		0.1538461540, // (245) 15:C-C 0b011110101
		1.0000000000, // (246) 15:G-G 0b011110110
		1.0000000000, // (247) 15:T-T 0b011110111
		0.0000000000, // (248) 15:A-A 0b011111000
		1.0000000000, // (249) 15:C-C 0b011111001
		0.0000000000, // (250) 15:G-G 0b011111010
		1.0000000000, // (251) 15:T-T 0b011111011
		1.0000000000, // (252) 15:A-A 0b011111100
		0.3461538460, // (253) 15:C-C 0b011111101
		0.6666666670, // (254) 15:G-G 0b011111110
		0.9090909090, // (255) 15:T-T 0b011111111
		0.1333333330, // (256) 16:A-A 0b100000000
		0.1764705880, // (257) 16:C-C 0b100000001
		0.1764705880, // (258) 16:G-G 0b100000010
		1.0000000000, // (259) 16:T-T 0b100000011
		0.4666666670, // (260) 16:A-A 0b100000100
		0.0588235290, // (261) 16:C-C 0b100000101
		1.0000000000, // (262) 16:G-G 0b100000110
		0.4666666670, // (263) 16:T-T 0b100000111
		0.2500000000, // (264) 16:A-A 0b100001000
		1.0000000000, // (265) 16:C-C 0b100001001
		0.2352941180, // (266) 16:G-G 0b100001010
		0.9333333330, // (267) 16:T-T 0b100001011
		1.0000000000, // (268) 16:A-A 0b100001100
		0.1176470590, // (269) 16:C-C 0b100001101
		0.7058823530, // (270) 16:G-G 0b100001110
		0.5333333330, // (271) 16:T-T 0b100001111
		0.5000000000, // (272) 17:A-A 0b100010000
		0.4000000000, // (273) 17:C-C 0b100010001
		0.1904761900, // (274) 17:G-G 0b100010010
		1.0000000000, // (275) 17:T-T 0b100010011
		0.6428571430, // (276) 17:A-A 0b100010100
		0.1333333330, // (277) 17:C-C 0b100010101
		1.0000000000, // (278) 17:G-G 0b100010110
		0.5384615380, // (279) 17:T-T 0b100010111
		0.6666666670, // (280) 17:A-A 0b100011000
		1.0000000000, // (281) 17:C-C 0b100011001
		0.4761904760, // (282) 17:G-G 0b100011010
		0.6923076920, // (283) 17:T-T 0b100011011
		1.0000000000, // (284) 17:A-A 0b100011100
		0.3333333330, // (285) 17:C-C 0b100011101
		0.4285714290, // (286) 17:G-G 0b100011110
		0.6666666670, // (287) 17:T-T 0b100011111
		0.5384615380, // (288) 18:A-A 0b100100000
		0.3750000000, // (289) 18:C-C 0b100100001
		0.2068965520, // (290) 18:G-G 0b100100010
		1.0000000000, // (291) 18:T-T 0b100100011
		0.4615384620, // (292) 18:A-A 0b100100100
		0.1250000000, // (293) 18:C-C 0b100100101
		1.0000000000, // (294) 18:G-G 0b100100110
		0.4285714290, // (295) 18:T-T 0b100100111
		0.6666666670, // (296) 18:A-A 0b100101000
		1.0000000000, // (297) 18:C-C 0b100101001
		0.4482758620, // (298) 18:G-G 0b100101010
		0.7142857140, // (299) 18:T-T 0b100101011
		1.0000000000, // (300) 18:A-A 0b100101100
		0.2500000000, // (301) 18:C-C 0b100101101
		0.2758620690, // (302) 18:G-G 0b100101110
		0.2857142860, // (303) 18:T-T 0b100101111
		0.6000000000, // (304) 19:A-A 0b100110000
		0.7647058820, // (305) 19:C-C 0b100110001
		0.2272727270, // (306) 19:G-G 0b100110010
		1.0000000000, // (307) 19:T-T 0b100110011
		0.3000000000, // (308) 19:A-A 0b100110100
		0.0588235290, // (309) 19:C-C 0b100110101
		1.0000000000, // (310) 19:G-G 0b100110110
		0.5000000000, // (311) 19:T-T 0b100110111
		0.7000000000, // (312) 19:A-A 0b100111000
		1.0000000000, // (313) 19:C-C 0b100111001
		0.4285714290, // (314) 19:G-G 0b100111010
		0.9375000000, // (315) 19:T-T 0b100111011
		1.0000000000, // (316) 19:A-A 0b100111100
		0.1764705880, // (317) 19:C-C 0b100111101
		0.0909090910, // (318) 19:G-G 0b100111110
		0.5625000000  // (319) 19:T-T 0b100111111
	};
	
	double cfdPamPenalties[16] = {
		0.0000000000, // (AA)
		0.0000000000, // (AC)
		0.2592592590, // (AG)
		0.0000000000, // (AT)
		0.0000000000, // (CA)
		0.0000000000, // (CC)
		0.1071428570, // (CG)
		0.0000000000, // (CT)
		0.0694444440, // (GA)
		0.0222222220, // (GC)
		1.0000000000, // (GG)
		0.0161290320, // (GT)
		0.0000000000, // (TA)
		0.0000000000, // (TC)
		0.0389610390, // (TG)
		0.0000000000  // (TT)
	};
	
    int maxDist = atoi(argv[3]);
    double threshold = atof(argv[4]);

    FILE *fp = fopen(argv[1], "rb");
    vector<size_t> slicelistHeader(6);
    if (fread(slicelistHeader.data(), sizeof(size_t), slicelistHeader.size(), fp) == 0) {
		fprintf(stderr, "Error reading index: header invalid\n");
		return 1;
	}
	
	offtargetsCount = slicelistHeader[0];
    seqLength       = slicelistHeader[1];
    seqCount        = slicelistHeader[2];
    sliceWidth      = slicelistHeader[3];
    sliceCount      = slicelistHeader[4];
    scoresCount     = slicelistHeader[5];
    
    size_t sliceLimit = 1 << sliceWidth;
    
	// read in the precalculated scores	
	//map<uint64_t, double> precalculatedScores;
	phmap::flat_hash_map<uint64_t, double> precalculatedScores;

	for (int i = 0; i < scoresCount; i++) {
		uint64_t mask = 0;
		double score = 0.0;
		fread(&mask, sizeof(uint64_t), 1, fp);
		fread(&score, sizeof(double), 1, fp);
		
		precalculatedScores.insert(pair<uint64_t, double>(mask, score));
	}
	
	// Load in all of the off-target sites
    vector<uint64_t> offtargets(offtargetsCount);
    if (fread(offtargets.data(), sizeof(uint64_t), offtargetsCount, fp) == 0) {
		fprintf(stderr, "Error reading index: loading off-target sequences failed\n");
		return 1;
	}
		
	// Create enough 1-bit "seen" flags for the off-targets
	// We only want to score a candidate guide against an off-target once.
	// The least-significant bit represents the first off-target
	// 0 0 0 1   0 1 0 0   would indicate that the 3rd and 5th off-target have been seen.
	// The CHAR_BIT macro tells us how many bits are in a byte (C++ >= 8 bits per byte)
	uint64_t numOfftargetToggles = (offtargetsCount / ((size_t)sizeof(uint64_t) * (size_t)CHAR_BIT)) + 1;

	
	vector<size_t> allSlicelistSizes(sliceCount * sliceLimit);
    vector<uint64_t> allSignatures(seqCount * sliceCount);
    
    if (fread(allSlicelistSizes.data(), sizeof(size_t), allSlicelistSizes.size(), fp) == 0) {
		fprintf(stderr, "Error reading index: reading slice list sizes failed\n");
		return 1;
	}
	
    if (fread(allSignatures.data(), sizeof(uint64_t), allSignatures.size(), fp) == 0) {
		fprintf(stderr, "Error reading index: reading slice contents failed\n");
		return 1;
	}
    fclose(fp);
    vector<vector<uint64_t *>> sliceLists(sliceCount, vector<uint64_t *>(sliceLimit));
    
    {
        uint64_t *offset = allSignatures.data();
        for (size_t i = 0; i < sliceCount; i++) {
            for (size_t j = 0; j < sliceLimit; j++) {
                size_t idx = i * sliceLimit + j;
                sliceLists[i][j] = offset;
                offset += allSlicelistSizes[idx];
            }
        }
    }
    
    size_t seqLineLength = seqLength + 1;
    size_t fileSize = getFileSize(argv[2]);
    if (fileSize % seqLineLength != 0) {
        fprintf(stderr, "Error: query file is not a multiple of the expected line length (%zu)\n", seqLineLength);
        fprintf(stderr, "The sequence length may be incorrect; alternatively, the line endings\n");
        fprintf(stderr, "may be something other than LF, or there may be junk at the end of the file.\n");
        exit(1);
    }
    size_t queryCount = fileSize / seqLineLength;
    fp = fopen(argv[2], "rb");
    vector<char> queryDataSet(fileSize);
    vector<uint64_t> querySignatures(queryCount);
    vector<double> querySignatureMitScores(queryCount);
    vector<double> querySignatureCfdScores(queryCount);

    if (fread(queryDataSet.data(), fileSize, 1, fp) < 1) {
        fprintf(stderr, "Failed to read in query file.\n");
        exit(1);
    }
    fclose(fp);

    #pragma omp parallel
    {
        #pragma omp for
        for (size_t i = 0; i < queryCount; i++) {
            char *ptr = &queryDataSet[i * seqLineLength];
            uint64_t signature = sequenceToSignature(ptr);
            querySignatures[i] = signature;
        }
    }

    #pragma omp parallel
    {
        unordered_map<uint64_t, unordered_set<uint64_t>> searchResults;
		vector<uint64_t> offtargetToggles(numOfftargetToggles);
    
		uint64_t * offtargetTogglesTail = offtargetToggles.data() + numOfftargetToggles - 1;

        #pragma omp for
        for (size_t searchIdx = 0; searchIdx < querySignatures.size(); searchIdx++) {

			auto searchSignature = querySignatures[searchIdx];

			double totScoreMit = 0.0;
			double totScoreCfd = 0.0;
            int numOffTargetSitesScored = 0;

            double maximum_sum = (10000.0 - threshold*100) / threshold;
			bool checkNextSlice = true;
			
            for (size_t i = 0; i < sliceCount; i++) {
                uint64_t sliceMask = sliceLimit - 1;
                int sliceShift = sliceWidth * i;
                sliceMask = sliceMask << sliceShift;
                auto &sliceList = sliceLists[i];
                
                uint64_t searchSlice = (searchSignature & sliceMask) >> sliceShift;
                
                size_t idx = i * sliceLimit + searchSlice;
                
                size_t signaturesInSlice = allSlicelistSizes[idx];
                uint64_t *sliceOffset = sliceList[searchSlice];
				
                for (size_t j = 0; j < signaturesInSlice; j++) {
                    auto signatureWithOccurrencesAndId = sliceOffset[j];
                    auto signatureId = signatureWithOccurrencesAndId & 0xFFFFFFFFull;

					uint64_t xoredSignatures = searchSignature ^ offtargets[signatureId];
					uint64_t evenBits = xoredSignatures & 0xAAAAAAAAAAAAAAAAull;
					uint64_t oddBits = xoredSignatures & 0x5555555555555555ull;
					uint64_t mismatches = (evenBits >> 1) | oddBits;
					int dist = __builtin_popcountll(mismatches);

					if (dist > 0 && dist <= maxDist) {
						uint64_t seenOfftargetAlready = 0;
						uint64_t * ptrOfftargetFlag = (offtargetTogglesTail - (signatureId / 64));
						if (i > 0) {
							seenOfftargetAlready = (*ptrOfftargetFlag >> (signatureId % 64)) & 1ULL;
						}
						
						if (!seenOfftargetAlready) {
							uint32_t occurrences = (signatureWithOccurrencesAndId >> (32));

							// Begin calculating CFD score
							double cfdScore = cfdPamPenalties[0b1010]; // PAM: NGG
							
							for (size_t pos = 0; pos < 20; pos++) {
								size_t mask = pos << 4;
								
								// Create the mask to look up the position-identity score
								// In Python... c2b is char to bit
								// 	mask = pos << 4
								// 	mask |= c2b[sgRNA[pos]] << 2
								// 	mask |= c2b[revcom(offTaret[pos])]
								
								// Find identity at `pos` for search signature
								// example: find identity in pos=2
								// 	Recall ISSL is inverted, hence:
								//              3'-  T  G  C  C  G  A -5'
								//	start		    11 10 01 01 10 00 	
								//	3UL << pos*2    00 00 00 11 00 00 
								//  and			    00 00 00 01 00 00
								//  shift		    00 00 00 00 01 00
								uint64_t searchSigIdentityPos = searchSignature;
								searchSigIdentityPos &= (3UL << (pos * 2));
								searchSigIdentityPos = searchSigIdentityPos >> (pos * 2); 
								searchSigIdentityPos = searchSigIdentityPos << 2;
								//std::cout << pos << "\t" << std::bitset<64>(searchSigIdentityPos) << "\t" << std::bitset<64>(searchSignature) << "\n";
								
								// Find identity at `pos` for offtarget
								// example: find identity in pos=2
								// 	Recall ISSL is inverted, hence:
								//              3'-  T  G  C  C  G  A -5'
								//	start		    11 10 01 01 10 00 	
								//	3UL<<pos*2      00 00 00 11 00 00 
								//  and			    00 00 00 01 00 00
								//  shift		    00 00 00 00 00 01
								//  rev comp 3UL    00 00 00 00 00 10 (done below)
								uint64_t offtargetIdentityPos = offtargets[signatureId];
								offtargetIdentityPos &= (3UL << (pos * 2));
								offtargetIdentityPos = offtargetIdentityPos >> (pos * 2); 

								// Complete the mask
								// reverse complement (^3UL) `offtargetIdentityPos` here
								mask = (mask | searchSigIdentityPos | (offtargetIdentityPos ^ 3UL));

								if (searchSigIdentityPos >> 2 != offtargetIdentityPos) {
									cfdScore *= cfdPosPenalties[mask];
								}
								
							}
							totScoreCfd += cfdScore;
							
							// Begin calculating MIT score
							totScoreMit += precalculatedScores[mismatches] * (double)occurrences;
							
							if (totScoreMit > maximum_sum) {
								checkNextSlice = false;
								break;
							}
							
							*ptrOfftargetFlag |= (1ULL << (signatureId % 64));

							numOffTargetSitesScored += occurrences;
						}
					}
                }
				
				if (!checkNextSlice)
					break;
            }
			
			querySignatureMitScores[searchIdx] = 10000.0 / (100.0 + totScoreMit);
			querySignatureCfdScores[searchIdx] = 10000.0 / (100.0 + totScoreCfd);

			memset(offtargetToggles.data(), 0, sizeof(uint64_t)*offtargetToggles.size());
        }
		
    }
	
	for (size_t searchIdx = 0; searchIdx < querySignatures.size(); searchIdx++) {
		auto querySequence = signatureToSequence(querySignatures[searchIdx]);
		printf("%s\t", querySequence.c_str());
		printf("%f\t", querySignatureMitScores[searchIdx]);
		printf("%f\n", querySignatureCfdScores[searchIdx]);
	}

    return 0;
}