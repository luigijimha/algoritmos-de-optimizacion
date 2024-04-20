#include <iostream>
#include <sstream>
#include <algorithm>
#include <vector>
#include <cmath>
using namespace std;

/* ----------------------------------------------------------------------------------------- */
/* ------------------------------------- Structures ---------------------------------------- */
/* ----------------------------------------------------------------------------------------- */

struct MatrixTuple {
    // stores sudoku tuple value
	int value;
    // pointer to its location inside ordered list
	struct DoubleLinkedOrderedList* pointer = NULL; // initialized with NULL
};

struct DoubleLinkedOrderedList {
    // position of tuple in matrix
    int row;
    int column;
    // all possible options of matrix tuple
	vector<int> possibleOptions;
    // next element of list
    struct DoubleLinkedOrderedList* next;
    // previous element of list
	struct DoubleLinkedOrderedList* previous;
};

/* ----------------------------------------------------------------------------------------- */
/* ------------------------------------- Prototypes ---------------------------------------- */
/* ----------------------------------------------------------------------------------------- */

MatrixTuple* newMatrixTuple(int value);
DoubleLinkedOrderedList* newDoubleLinkedOrderedList(int row, int column, vector<int> possibleOptions);
void insert(DoubleLinkedOrderedList** list, int row, int column, vector<int> possibleOptions, MatrixTuple* tuple);
void remove(DoubleLinkedOrderedList* element, int value);
vector<int> findPossibleOptions(vector<vector<MatrixTuple*>>* matrix, int row, int column);
void markTuple(vector<vector<MatrixTuple*>>* matrix, DoubleLinkedOrderedList* element);
void printMatrix(vector<vector<MatrixTuple*>>* matrix);
void printList(DoubleLinkedOrderedList* list);
void printNextListData(DoubleLinkedOrderedList* list);

/* ----------------------------------------------------------------------------------------- */
/* ---------------------------------------- Main ------------------------------------------- */
/* ----------------------------------------------------------------------------------------- */

int main() {
    // read user input
    // 0 means it is an empty tile

    vector<vector<int>> inputMatrix = {
        {8, 0, 0, 5, 0, 7, 0, 9, 0},
        {0, 2, 9, 0, 0, 4, 0, 0, 6},
        {3, 0, 0, 2, 0, 0, 0, 0, 0},
        {0, 8, 0, 0, 0, 6, 5, 0, 1},
        {0, 1, 7, 4, 0, 0, 0, 3, 0},
        {2, 0, 0, 0, 0, 1, 0, 0, 0},
        {0, 9, 4, 1, 0, 0, 8, 7, 0},
        {0, 0, 8, 6, 0, 0, 0, 0, 0},
        {0, 5, 0, 0, 7, 0, 0, 0, 3}
    };
    
    vector<vector<MatrixTuple*>> sudokuMatrix(9, vector<MatrixTuple*>(9));

    // Store input in matrix
    for(int row = 0; row < 9; ++row) {
        for(int column = 0; column < 9; ++column) {
            int tupleValue = inputMatrix[row][column];
            sudokuMatrix[row][column] = newMatrixTuple(tupleValue);
        }
    }

    // build ordered list
    DoubleLinkedOrderedList* list = NULL;
    for(int row = 0; row < 9; ++row) {
        for(int column = 0; column < 9; ++column) {
            if(sudokuMatrix[row][column]->value == 0) {
                // find possible options
                vector<int> possibleOptions = findPossibleOptions(&sudokuMatrix, row, column);
                insert(&list, row, column, possibleOptions, sudokuMatrix[row][column]);
            }
        }
    }

    //? debug
    printMatrix(&sudokuMatrix);
    //printList(list);
    //printNextListData(list);

    // iterate over list and update matrix values
    while(list != NULL) {
        // verify if problem has a unique solution
        if(list->possibleOptions.size() > 1) {
            cout << "the problem doesn't have an obvious solution or it has multiple solutions" << endl;
            break;
        }

        // mark value in board with tuple solution found
        markTuple(&sudokuMatrix, list);

        // remove element from list
        DoubleLinkedOrderedList* temp = list;
        list = list->next;
        if(list) {
            list->previous = NULL;
        }
        free(temp);

        printMatrix(&sudokuMatrix);
        // debug
        //printList(list);
    }
}

/* ----------------------------------------------------------------------------------------- */
/* ---------------------------------- Malloc Functions ------------------------------------- */
/* ----------------------------------------------------------------------------------------- */

/**
 * constructor for MatrixTuple
 * @param{int} value    matrix tuple value
 * @return              MatrixTuple memory reference
*/
MatrixTuple* newMatrixTuple(int value) {
    struct MatrixTuple* object = new MatrixTuple;
    object->value = value;
    object->pointer = NULL;

    return object;
}

/**
 * constructor for DoubleLinkedOrderedList
 * @param {int} row                    row index where matrix tile is located
 * @param {int} column                 column index where matrix tile is located
 * @param {vector} possibleOptions    array with all possible numbers for matrix tile
 * @return                             DoubleLinkedOrderedList memory reference
*/
DoubleLinkedOrderedList* newDoubleLinkedOrderedList(int row, int column, vector<int> possibleOptions) {
    struct DoubleLinkedOrderedList* object = new DoubleLinkedOrderedList;
    object->row = row;
    object->column = column;
    object->possibleOptions = possibleOptions;
    object->next = NULL;
    object->previous = NULL;

    return object;
}

/* ----------------------------------------------------------------------------------------- */
/* ----------------------------- Ordered Structure Functions ------------------------------- */
/* ----------------------------------------------------------------------------------------- */

/**
 * register MatrixTuple into DoubleLinkedOrderedList
 * @param {DoubleLinkedOrderedList**} list    memory reference to start of the list
 * @param {int} row                           row index where matrix tile is located
 * @param {int} column                        column index where matrix tile is located
 * @param {vector} possibleOptions            array with all possible numbers for matrix tile
 * @param {MatrixTuple* tuple}                reference to MatrixTuple to register
*/
void insert(DoubleLinkedOrderedList** list, int row, int column, vector<int> possibleOptions, MatrixTuple* tuple){
    DoubleLinkedOrderedList* element = newDoubleLinkedOrderedList(row, column, possibleOptions);
    tuple->pointer = element;

    // If the list is empty or the new element should be inserted at the beginning
    if (*list == NULL || (*list)->possibleOptions.size() >= possibleOptions.size()) {
        element->next = *list;
        if (*list != NULL) {
            (*list)->previous = element;
        }
        *list = element;
        return;
    }

    DoubleLinkedOrderedList* current = *list;
    // Traverse the list to find the correct position to insert the new element
    while (current->next != NULL && current->next->possibleOptions.size() < possibleOptions.size()) {
        current = current->next;
    }
    element->next = current->next;
    if (current->next != NULL) {
        current->next->previous = element;
    }
    current->next = element;
    element->previous = current;
}

/**
 * discards option from MatrixTuple possible options and reorders its position in DoubleLinkedOrderedList
 * @param {DoubleLinkedOrderedList*} element    DoubleLinkedOrderedList element
 * @param {int} value                           option to remove from list
*/
void remove(DoubleLinkedOrderedList* element, int value) {
    // remove value from vector
    element->possibleOptions.erase(find(element->possibleOptions.begin(), element->possibleOptions.end(), value));

    // update element position in ordered list
    DoubleLinkedOrderedList* current = element->previous;

    // look for position to reposition element
    while (current->previous != NULL && current->possibleOptions.size() > element->possibleOptions.size()) {
        current = current->previous;
    }

    element->previous->next = element->next;
    if(element->next) {
        element->next->previous = element->previous;
    }

    element->previous = current;
    element->next = current->next;
    if(current->next) {
        current->next->previous = element;
    }
    current->next = element;
}

/* ----------------------------------------------------------------------------------------- */
/* ------------------------------- Sudoku Matrix Functions --------------------------------- */
/* ----------------------------------------------------------------------------------------- */

/**
 * finds possible options for MatrixTuple by discarding repeated values in its row, column and segment group
 * @param{vector} matrix    sudoku matrix
 * @param{int} row          row index where MatrixTuple is located at
 * @param{int} column       column index where MatrixTuple is located at
 * @return                  array with all possible options for that tile
*/
vector<int> findPossibleOptions(vector<vector<MatrixTuple*>>* matrix, int row, int column){
    vector<int> possibleOptions = {1, 2, 3, 4, 5, 6, 7, 8, 9};

    // values used to identify sudoku group section
    int rowStartGroup = row - (row % 3);
    int columnStartGroup = column - (column % 3);

    // look for repeated values in the row and column
    for(int i = 0; i < 9; ++i) {
        int rowValue = (*matrix)[row][i]->value;
        int columnValue = (*matrix)[i][column]->value;
        int groupValue = (*matrix)[ rowStartGroup + i%3 ][ columnStartGroup + i/3 ]->value;

        // remove repeated value
        if(find(possibleOptions.begin(), possibleOptions.end(), rowValue) != possibleOptions.end()){
            possibleOptions.erase(find(possibleOptions.begin(), possibleOptions.end(), rowValue));
        }
        if(find(possibleOptions.begin(), possibleOptions.end(), columnValue) != possibleOptions.end()) {
            possibleOptions.erase(find(possibleOptions.begin(), possibleOptions.end(), columnValue));
        }
        if(find(possibleOptions.begin(), possibleOptions.end(), groupValue) != possibleOptions.end()) {
            possibleOptions.erase(find(possibleOptions.begin(), possibleOptions.end(), groupValue));
        }
    }

    return possibleOptions;
}

/**
 * registers value found in sudoku matrix and updates other MatrixTuple status in the same row, column and segment group
 * @param{vector} matrix                       reference to sudoku matrix
 * @param{DoubleLinkedOrderedList*} element    element on DoubleLinkedOrderedList which will be used to update sudoku matrix
*/
void markTuple(vector<vector<MatrixTuple*>>* matrix, DoubleLinkedOrderedList* element) {
    int changedRow = element->row;
    int changedColumn = element->column;
    int changedRowGroup = changedRow - (changedRow % 3);
    int changedColumnGroup = changedColumn - (changedColumn % 3);
    // index 0 is used because it is assumed that you've found the correct value, thus you only have one possible option
    int value = element->possibleOptions[0];

    // update tuple with the only answer value
    (*matrix)[changedRow][changedColumn]->value = value;

    // remove pointer from tuple since final value has been found
    (*matrix)[changedRow][changedColumn]->pointer = NULL;

    // update values in changed sections
    for(int i = 0; i < 9; ++i) {
        MatrixTuple* affectedRow = (*matrix)[changedRow][i];
        MatrixTuple* affectedColumn = (*matrix)[i][changedColumn];
        MatrixTuple* affectedGroup = (*matrix)[ changedRowGroup + i/3 ][ changedColumnGroup + i%3 ];
        // remove repeated value from matrix changed elements and update ordered structure
        if( // ignore tuples with data
            affectedRow->value == 0 &&
            find(affectedRow->pointer->possibleOptions.begin(), affectedRow->pointer->possibleOptions.end(), value) != affectedRow->pointer->possibleOptions.end()) {
            remove((*matrix)[changedRow][i]->pointer, value);
        }
        if( // ignore tuples with data
            affectedColumn->value == 0 &&
            find(affectedColumn->pointer->possibleOptions.begin(), affectedColumn->pointer->possibleOptions.end(), value) != affectedColumn->pointer->possibleOptions.end()) {
            remove((*matrix)[i][changedColumn]->pointer, value);
        }
        if( // ignore tuples with data
            affectedGroup->value == 0 &&
            find(affectedGroup->pointer->possibleOptions.begin(), affectedGroup->pointer->possibleOptions.end(), value) != affectedGroup->pointer->possibleOptions.end()) {
            remove((*matrix)[ changedRowGroup + i/3 ][ changedColumnGroup + i%3 ]->pointer, value);
        }
    }
}

/**
 * prints formatted sudoku matrix
 * @param{vector} matrix    reference to matrix
*/
void printMatrix(vector<vector<MatrixTuple*>>* matrix) {
    for (int row = 0; row < 9; ++row) {
        if (row % 3 == 0 && row != 0) {
            // Print horizontal line separator
            cout << "- - - - - - - - - - - - - - - -" << endl;
        }
        for (int column = 0; column < 9; ++column) {
            if (column % 3 == 0 && column != 0) {
                // Print vertical line separator
                cout << " |";
            }
            MatrixTuple* tile = (*matrix)[row][column];
            if (tile->value != 0) {
                // Print tile value
                cout << " " << tile->value << " ";
            } else {
                // Print placeholder for empty tile
                cout << " - ";
            }
        }
        cout << endl;
    }
    cout << "\n= = = = = = = = = = = = = = = =\n\n";
}

/* ----------------------------------------------------------------------------------------- */
/* ----------------------------------- Debug Functions ------------------------------------- */
/* ----------------------------------------------------------------------------------------- */

/**
 * prints ordered list contents, it is used to verify pointes are correctly set
 * @param{DoubleLinkedOrderedList*} list    reference to the start of the list
*/
void printList(DoubleLinkedOrderedList* list) {
    if(!list) {
        cout << "list is empty" << endl;
        return;
    }

    // print list from start to end
    cout << "list from start to end";
    while(list->next) {
        cout << "(" << list->column << ", " << list->row << ") -> ";
        list = list->next;
    }
    cout << "(" << list->column << ", " << list->row << ")\n\n";

    // print list from end to start
    cout << "list from end to start";
    while(list->previous) {
        cout << "(" << list->column << ", " << list->row << ") -> ";
        list = list->previous;
    }
    cout << "(" << list->column << ", " << list->row << ")\n\n";
}

/**
 * prints data inside the first element of the list
 * @param{DoubleLinkedOrderedList*} list    reference to the start of the list
*/
void printNextListData(DoubleLinkedOrderedList* list) {
    if(!list) {
        cout << "list is empty" << endl;
        return;
    }

    cout << "next element: " << endl;
    cout << "(" << list->column << ", " << list->row << ")" << endl;
    cout << "possible options: (";
    for(int it: list->possibleOptions) {
        cout << it << " " ;
    }
    cout << ")\n\n";
}

// sample output
/*
8 4 1  | 5 6 7  | 3 9 2 
5 2 9  | 3 1 4  | 7 8 6
3 7 6  | 2 8 9  | 1 5 4
- - - - - - - - - - - -
4 8 3  | 7 9 6  | 5 2 1
9 1 7  | 4 5 2  | 6 3 8
2 6 5  | 8 3 1  | 9 4 7
- - - - - - - - - - - -
6 9 4  | 1 2 3  | 8 7 5
7 3 8  | 6 4 5  | 2 1 9
1 5 2  | 9 7 8  | 4 6 3
*/