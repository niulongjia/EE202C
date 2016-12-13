#include "fann.h"
#include <iostream>
#include "parameters.h"

using namespace std;

int main()
{  
    struct fann *ann = fann_create_standard(num_layers, num_input,
        num_neurons_hidden, num_output);

    fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC);
    fann_set_activation_function_output(ann, FANN_SIGMOID_SYMMETRIC);
    //fann_set_learning_rate(ann,0.300000);
    //fann_set_learning_momentum(ann, 0.90000);
    //fann_set_training_algorithm(ann, FANN_TRAIN_QUICKPROP);
    
    // The first line of train_data_file should be: 
    // lines coefficients states.
    fann_train_on_file(ann, train_data_file, max_epochs,
        epochs_between_reports, desired_error);

    fann_save(ann, output_neuro_file);

    fann_destroy(ann);

    return 0;
}
