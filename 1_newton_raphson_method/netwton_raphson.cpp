#include <bits/stdc++.h>
using namespace std;

float absolute(float x);
string rpad(float number);

int main() {
	float xOld, xNew;
	float error;
	int max_iterations;
    
    cout << "input starting value: ";
    cin >> xNew;
    cout << "input max iterations: ";
    cin >> max_iterations;
    cout << endl;
    
    cout << "xi              f(x)            f'(x)           x(i+1)          error          " << endl;

    do {
        // set x value
        xOld = xNew;
        // calculate f(x)
        float function = sin(xOld) - 2 / (1 + xOld*xOld);
        // calculate f'(x)
        float dfunction = cos(xOld) + (4 * xOld) / (1 + 2*xOld*xOld + xOld*xOld*xOld*xOld);
        // get x(i+1)
        xNew = xOld - function / dfunction;
        // calculate error
        error = xOld - xNew;
        
        cout << rpad(xOld) << " "
            << rpad(function) << " "
            << rpad(dfunction) << " "
            << rpad(xNew) << " "
            << rpad(error) << endl;
            
    } while(absolute(error) > 0.00000001 && --max_iterations);
    
    if (max_iterations) {
        cout << endl << "root is located at " << xNew;   
    } else {
        cout << endl << "maximum iterations reached";
    }
    
    return 0;
}

/**
 * returns the absolute value of a number
 * @param {float}    float number
 * @return           absolute value of float number
*/
float absolute(float x) {
    return x < 0 ? x * -1 : x;
}

/**
 * gives padding format to a number for the printing table
 * @param {float}    number to print in table
 * @return           formatted number with spaces
*/
string rpad(float number) {
    string message = to_string(number);
    return message + string(15 - message.length(), ' ');
}