#include <iostream>
#include <vector>
#include <map>
#include <algorithm>
using namespace std;

int sumArray(map<int, int> arr);
vector<int> getCombinations(map<int, int> arr);
int findZeroes(vector<int> positives, vector<int> negatives);

int main() {
    // stores the amount of repetitions of each positive number
    map<int, int> positives;
    // stores the amount of repetitions of each negative number
    map<int, int> negatives;
    // stores total 0s
    int zeroes = 0;
    // total input of elements
    int n;

    cout << "Insert array length: ";
    cin >> n;
    cout << "Insert array (ex. 1 2 3 4): " << endl;
    // store positive, negative and zero numbers in their respective variables
    while(n--) {
        int x;
        cin >> x;
        if(x < 0) {
            negatives[x*-1] = negatives[x*-1] + 1;
        } else if(x > 0) {
            positives[x*1] = positives[x*1] + 1;
        } else {
            ++zeroes;
        }
    }

    // get total positive and negative combinations
    vector<int> positive_combinations = getCombinations(positives);
    vector<int> negative_combinations = getCombinations(negatives);

    // calculate total posible combinations
    int total_combinations = findZeroes(positive_combinations, negative_combinations) * (zeroes + 1) + zeroes;

    cout << "total combinations: " << total_combinations;

    return 0;
}

/**
 * sums the maximum number obtainable in an array
 * @param {Object}    map who counts the amount of repetitions a number has
 * @return {int}      the maximum number obtainable from the sum of all the numbers
*/
int sumArray(map<int, int> arr) {
    int sum = 0;

    for(pair<int, int> i : arr) {
        sum += i.first * i.second;
    }

    return sum;
}

/**
 * get all posible combinations from array set of data
 * @param {Object}     map who has the amount of repetitions each number has in array
 * @return {Object}    the amount of possible combinations up to max number possible of array
*/
vector<int> getCombinations(map<int, int> arr) {
    // calculate the maximum number obtainable from array
    int max = sumArray(arr);

    // initialize n empty vectors
    vector<vector<map<int, int>>> combinations(max + 1);

    vector<int> response;

    for(int i = 1; i <= max; ++i) {
        for(int j = 1; j <= i/2; ++j) {
            // iterate over all combinations of two numbers that can create that number
            vector<map<int, int>> row1 = combinations[j];
            vector<map<int, int>> row2 = combinations[i-j];

            int possibleCombinations = row1.size() * row2.size();

            for(int k = 0; k < possibleCombinations; ++k) {
                map<int, int> combination1 = row1[k % row1.size()];
                map<int, int> combination2 = row2[k / row1.size()];

                map<int, int> combination;

                // merge numbers required for both combination
                map<int, int>::iterator it1 = combination1.begin();
                map<int, int>::iterator it2 = combination2.begin();

                // merge possible repeated elements
                while(it1 != combination1.end() && it2 != combination2.end()) {
                    if((*it1).first == (*it2).first) {
                        combination[(*it1).first] = (*it1).second + (*it2).second;
                        ++it1;
                        ++it2;
                    } else if ((*it1).first < (*it2).first) {
                        combination[(*it1).first] = (*it1).second;
                        ++it1;
                    } else {
                        combination[(*it2).first] = (*it2).second;
                        ++it2;
                    }
                }
                
                // merge remaining elements inside map
                combination.insert(
                    (it1 == combination1.end() ? it2 : it1),
                    (it1 == combination1.end() ? combination2.end() : combination1.end())
                );

                // verify if you have enough numbers to use each combination
                bool isPossible = true;

                for(const auto& [number, repetitions] : combination) {
                    if(arr[number] < repetitions) {
                        // not enough numbers for combination
                        isPossible = false;
                        break;
                    }
                }

                if(isPossible &&
                    // verify if combination doesn't exists
                    find(combinations[i].begin(), combinations[i].end(), combination) == combinations[i].end()) {
                    // add complete combination to combination list
                    combinations[i].push_back(combination);
                }

            }
        }

        // verify if you have the actual number in array and add it as unique combination
        if (arr[i] != 0) {
            combinations[i].push_back({{i, 1}});
        }
        
    }

    // fill up response with combinations found
    for(int i = 1; i <= max; ++i) {
        response.push_back(combinations[i].size());
    }

    return response;
}

/**
 * calculates the amount of zeroes obtained based on positive and negative combinations for each number
 * @param {Object} positives    array with possible positive combinations up to n
 * @param {Object} negatives    array with possible negative combinations up to m
 * @return {int}                the amount of sum zero combination posible from positive and negative numbers
*/
int findZeroes(vector<int> positives, vector<int> negatives) {
    int zeroes = 0;
    int limit = positives.size() < negatives.size() ? positives.size() : negatives.size();

    for(int i = 0; i < limit; ++i) {
        zeroes += positives[i] * negatives[i];
    }

    return zeroes;
}

/*
test case
9
1 1 1 2 -1 -1 -2 -3 0

expected answer: 27 combinations
*/