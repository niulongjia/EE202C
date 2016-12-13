CC=g++
LDFLAGS=-lmraa -lfann
CFLAGS=-Wall
SOURCES=test_neural_network.c train_neural_net.c test_neural_network_listener.c
EXECUTABLES=$(SOURCES:.c=)

all: test_neural_network train_neural_net test_neural_network_listener

test_neural_network: test_neural_network.c
	$(CC) $(CFLAGS) -o test_neural_network test_neural_network.c $(LDFLAGS)

train_neural_net: train_neural_net.c
	$(CC) $(CFLAGS) -o train_neural_net train_neural_net.c $(LDFLAGS)
 
test_neural_network_listener: test_neural_network_listener.c
	$(CC) $(CFLAGS) -o test_neural_network_listener test_neural_network_listener.c $(LDFLAGS)
 
clean:
	rm -f test_neural_network
	rm -f train_neural_net
	rm -f test_neural_network_listener
	rm -f *~
	rm -f TEST.net
	rm -f test_data.txt