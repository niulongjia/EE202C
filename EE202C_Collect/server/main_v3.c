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
//pthread_mutex_t exec_mutex;

char wrist[256];
char elbow[256];

/* Detect the motion */
void predict(){
	FILE *fp_wrist;
	FILE *fp_elbow;

	fp_wrist = fopen(wrist,"r");
	fp_elbow = fopen(elbow,"r");
	if(fp_wrist != NULL){
		fseek(fp_wrist,0,SEEK_END);
		unsigned long len = (unsigned long) ftell(fp_wrist);
		printf("wrist size = %lu\n",len);
		fclose(fp_wrist);
	}
	

	if(fp_elbow != NULL){
		fseek(fp_elbow,0,SEEK_END);
		unsigned long len = (unsigned long) ftell(fp_elbow);
		printf("elbow size = %lu\n",len);
		fclose(fp_elbow);
	}
	
	// data analysis	
	//if(fp_wrist != NULL) fclose(fp_wrist);
	//if(fp_elbow != NULL) fclose(fp_elbow);

	FILE *empty_wrist = fopen(wrist,"w"); 
	FILE *empty_elbow = fopen(elbow,"w");
	/*
	if(empty_wrist != NULL){
		fseek(empty_wrist,0,SEEK_END);
		unsigned long len = (unsigned long) ftell(empty_wrist);
		printf("wrist size = %lu\n",len);
	}
	

	if(empty_elbow != NULL){
		fseek(empty_elbow,0,SEEK_END);
		unsigned long len = (unsigned long) ftell(empty_elbow);
		printf("elbow size = %lu\n",len);
	}
	*/
	if(empty_wrist != NULL) fclose(empty_wrist);
	if(empty_elbow != NULL) fclose(empty_elbow);
}

/* Interrupt every 5 seconds */
void time_window_alarm(){
	//pthread_mutex_lock(&exec_mutex);
	collect_flag = 0;
	//printf("GET LOCK!\n");
	predict();
	alarm(5);
	collect_flag = 1;
	//printf("RELEASE LOCK!\n");
	//pthread_mutex_unlock(&exec_mutex);
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
		//pthread_mutex_lock(&exec_mutex);
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
		//pthread_mutex_unlock(&exec_mutex);		
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
	
	client = (CONNECTION *)arg;

	client_socket_fd = client->sockfd;

	memset(buffer, 0, 256);
	sprintf(buffer, "output_file_IP_%s_TIMESTAMP_%u.csv\n", client->ip_addr_str, (unsigned)time(NULL));

	/* Initialize files */
	memset(tmp,0,256);
	memset(wrist,0,256);
	memset(elbow,0,256);
	n = read(client_socket_fd,tmp,255);

	if((strcmp(tmp,"NINEDOF_2_WRIST")) == 0){
		sprintf(wrist,buffer);
	}
	else if((strcmp(tmp,"NINEDOF_3_ELBOW")) == 0){
		sprintf(elbow,buffer);
	}
	printf("filename: %s", buffer);

	fp = fopen(buffer, "wb");

	while (run_flag) {
		if(collect_flag){
		// pthread_mutex_lock(&exec_mutex);
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
		// printf("%s says: %s\n", client->ip_addr_str, buffer);
		fprintf(fp, "%s\n", buffer);

		// send an acknowledgement back to the client saying that we received the message
		memset(tmp, 0, sizeof(tmp));
		sprintf(tmp, "%s sent the server: %s", client->ip_addr_str, buffer);
		n = write(client_socket_fd, tmp, strlen(tmp));
		if (n < 0) {
			server_error("ERROR writing to socket");
			return NULL;
		}
		}
		// pthread_mutex_unlock(&exec_mutex);
	}

	fclose(fp);
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

	i = -1;

	while(i < max_connections && run_flag) {
		if(collect_flag){
		//pthread_mutex_lock(&exec_mutex);
		client = (CONNECTION*) server_accept_connection(server->sockfd);
		if ((int) client == -1) {
			printf("Latest child process is waiting for an incoming client connection.\n");
		}
		else {
			i++;
			pthread_create(&tids[i], NULL, handle_client, (void *)client);
		}
		//pthread_mutex_unlock(&exec_mutex);
		}
	}

	if (i >= max_connections) {
		printf("Max number of connections reached. No longer accepting connections. Continuing to service old connections.\n");
	}


	for(; i >= 0; i--) {
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
	alarm(10);
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
