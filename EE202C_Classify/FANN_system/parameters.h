#include <string>
using namespace std; // to use string

const unsigned int num_input = 90; // coefficients
const unsigned int num_output = 6; // states
const unsigned int num_layers = 3;
const unsigned int num_neurons_hidden = 180;
const float desired_error = (const float) 0.001;
const unsigned int max_epochs = 5000000;
const unsigned int epochs_between_reports = 100;
const char* train_data_file = "coefficient_data_train.txt";
const char* output_neuro_file = "TEST.net";
const char* test_data_file = "coefficient_data_test.txt";
const char* prediction_results_file = "prediction_results.txt";
const int coefficients_num = 90; // coefficients
const int states_num = 6; // states

//extern const int global_variable;
