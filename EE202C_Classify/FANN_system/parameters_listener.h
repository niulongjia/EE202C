#include <string>
using namespace std; // to use string

const unsigned int num_input = 90; // coefficients
const unsigned int num_output = 6; // states
const unsigned int num_layers = 3;
const unsigned int num_neurons_hidden = 180;
const float desired_error = (const float) 0.001;
const unsigned int max_epochs = 5000000;
const unsigned int epochs_between_reports = 100;

const char* output_neuro_file = "TEST.net";
const char* test_data_file = "coefficient_data_test_update.txt"; // generated from python.
const char* prediction_result_file = "prediction_result_update.txt";
const char* prediction_result_html_file = "/usr/share/apache2/htdocs/prediction_update.html";
const int coefficients_num = 90; // coefficients
const int states_num = 6; // states

//extern const int global_variable;
