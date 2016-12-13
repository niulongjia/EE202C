//#include <iostream>
//#include <fstream>
#include <stdio.h>
#include <string.h>

#include <sys/types.h>
#include <signal.h>
#include <pthread.h>

#include "server.h"
#include "9DOF.h"
#include "LSM9DS0.h"

//using namespace std;

#define PORTNO 5000

static volatile int run_flag = 1;
static volatile int collect_flag = 1;
static volatile int num_clients = -1;
static volatile int trial = 1;

static FILE *fp1;
static FILE *fp2;
static FILE *fp3;

/* Detect the motion */
void predict(){
	if(fp1 != NULL) fclose(fp1);
	if(fp2 != NULL) fclose(fp2);
	if(fp3 != NULL) fclose(fp3);
	trial++;
	fp1 = NULL;
	fp2 = NULL;
	fp3 = NULL;;
	char buffer[256];
	memset(buffer,0,256);
	sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_3_LEFT_WRIST_%d.csv",trial);
	fp3 = fopen(buffer,"w+");
	memset(buffer,0,256);
	sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_2_RIGHT_ELBOW_%d.csv",trial);
	fp2 = fopen(buffer,"w+");
	memset(buffer,0,256);
	sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_1_RIGHT_WRIST_%d.csv",trial);
	fp1 = fopen(buffer,"w+");
}

/* Interrupt every 5 seconds */
void time_window_alarm(){
	collect_flag = 0;
	predict();
	alarm(10);
	collect_flag = 1;
}

void do_when_interrupted()
{
	run_flag = 0;
	printf("\n Threads exiting. Please wait for cleanup operations to complete...\n");
}

double timestamp()
{
	// calculate and return the timestamp
	struct timeval tv;
	double sec_since_epoch;

	gettimeofday(&tv, NULL);
	sec_since_epoch = (double) tv.tv_sec + (double) tv.tv_usec/1000000.0;

	return sec_since_epoch;
}

void* manage_9dof(void *arg) 
{
	NINEDOF *ninedof;
	double sec_since_epoch;

	mraa_init();

	FILE *fp;
	fp = fopen("./server_test_data.csv", "w");

	// write header to file "test_data.csv"
	fprintf(fp, "time (epoch), accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z, mag_x, mag_y, mag_z, temperature");
	fclose(fp);
	
	// 9DOF sensor initialization
	ninedof = ninedof_init(A_SCALE_4G, G_SCALE_245DPS, M_SCALE_2GS);

	while(run_flag) {
		if(collect_flag){
			// timestamp right before reading 9DOF data
			sec_since_epoch = timestamp();
			ninedof_read(ninedof);

			// append 9DOF data with timestamp to file "server_test_data.csv"
			fp = fopen("./server_test_data.csv", "a");
			fprintf(fp, "%10.10f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n", sec_since_epoch,
			ninedof->accel_data.x, ninedof->accel_data.y, ninedof->accel_data.z,
			ninedof->gyro_data.x - ninedof->gyro_offset.x, 
  			ninedof->gyro_data.y - ninedof->gyro_offset.y, 
  			ninedof->gyro_data.z - ninedof->gyro_offset.z,
 			ninedof->mag_data.x, ninedof->mag_data.y, ninedof->mag_data.z,
  			ninedof->temperature);
			fclose(fp);

			// print server 9DOF data
			// ninedof_print(ninedof);
			usleep(10000);
		}
	}

	return NULL;
}

void* handle_client(void *arg)
{
	CONNECTION *client;
	int n, client_socket_fd;
	char buffer[256], tmp[256];
	FILE *fp;
	int position = -1;
	client = (CONNECTION *)arg;

	client_socket_fd = client->sockfd;

	memset(buffer, 0, 256);
	//sprintf(buffer, "output_file_IP_%s_TIMESTAMP_%u.csv\n", client->ip_addr_str, (unsigned)time(NULL));

	/* Initialize files */
	memset(tmp,0,256);
	n = read(client_socket_fd,tmp,256);
	printf(tmp);
	if((strcmp(tmp,"NINEDOF_3_LEFT_WRIST")) == 0){
		sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_3_LEFT_WRIST_%d.csv",trial);
		fp3 = fopen(buffer,"w");
		position = 3;	
	}else if((strcmp(tmp,"NINEDOF_2_RIGHT_ELBOW")) == 0){
		sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_2_RIGHT_ELBOW_%d.csv",trial);
		fp2 = fopen(buffer,"w");
		position = 2;
	}else if((strcmp(tmp,"NINEDOF_1_RIGHT_WRIST"))== 0){
		sprintf(buffer,"/home/root/UpperBodyClassification/MachineLearning/FANN_system/NINEDOF_1_RIGHT_WRIST_%d.csv",trial);
		fp1 = fopen(buffer,"w");
		position = 1;
	}
	printf("filename: %s", buffer);

	while (run_flag) {
		if(collect_flag){
			if(position == 1) fp = fp1;
			if(position == 2) fp = fp2;
			if(position == 3) fp = fp3;
			// clear the buffer
			memset(buffer, 0, 256);
			// read what the client sent to the server and store it in "buffer"
			n = read(client_socket_fd, buffer, 255);	
			// an error has occurred
			if (n < 0) {
				server_error("ERROR reading from socket");
				return NULL;
			}
			// no data was sent, assume the connection was terminated
			if (n == 0) { 
				printf("%s has terminated the connection.\n", client->ip_addr_str);
				return NULL;
			}

			// print the message to console
			if(num_clients >= 2) fprintf(fp, "%s\n", buffer);
			//n = fprintf(fp, "%s\n", buffer);
			//printf("***writing to file %i *** %i *** %i\n", trial,  position,n);

			// send an acknowledgement back to the client saying that we received the message
			memset(tmp, 0, sizeof(tmp));
			sprintf(tmp, "%s sent the server: %s", client->ip_addr_str, buffer);
			n = write(client_socket_fd, tmp, strlen(tmp));
			if (n < 0) {
				server_error("ERROR writing to socket");
				return NULL;
			}
		}
	}

	if(fp1 != NULL) fclose(fp1);
	if(fp2 != NULL) fclose(fp2);
	if(fp3 != NULL) fclose(fp3);
	close(client_socket_fd);
	return NULL;
}

void* manage_server(void *arg)
{
	CONNECTION *server;
	CONNECTION *client;
	int max_connections;
	int i;
	pthread_t tids[256];

	max_connections = 10;

	server = (CONNECTION *) server_init(PORTNO, 10);
	if ((int) server == -1){
		run_flag = 0;
	}

	while(num_clients < max_connections && run_flag) {
		if(collect_flag){
			client = (CONNECTION*) server_accept_connection(server->sockfd);
			if ((int) client == -1) {
				printf("Latest child process is waiting for an incoming client connection.\n");
			}
			else {
				num_clients++;
				pthread_create(&tids[num_clients], NULL, handle_client, (void *)client);
			}
		}
	}

	if (num_clients >= max_connections) {
		printf("Max number of connections reached. No longer accepting connections. Continuing to service old connections.\n");
	}


	for(i = num_clients; i >= 0; i--) {
		pthread_join(tids[i], NULL);
	}

	return NULL;
}

int main(int argc, char **argv)
{
	pthread_t manage_9dof_tid, manage_server_tid;
	int rc;

	signal(SIGINT, do_when_interrupted);

	/* ALARM --> */
	signal(SIGALRM, time_window_alarm);
	alarm(25);
	/* <-- ALARM */

	rc = pthread_create(&manage_9dof_tid, NULL, manage_9dof, NULL);
	if (rc != 0) {
		fprintf(stderr, "Failed to create manage_9dof thread. Exiting Program.\n");
		exit(0);
	}

	rc = pthread_create(&manage_server_tid, NULL, manage_server, NULL);
	if (rc != 0) {
		fprintf(stderr, "Failed to create thread. Exiting program.\n");
		exit(0);
	}

	pthread_join(manage_9dof_tid, NULL);
	pthread_join(manage_server_tid, NULL);

	printf("\n...cleanup operations complete. Exiting main.\n");

	return 0;
}
