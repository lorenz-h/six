# Six
Six is an affective AI.
## Structure
Some components such as Six Chat can be run independently on endpoints such as mobile devices, while the main instance of six is run on a remote server. Communication between the components is handled by a GenericCommInterface Subclass from spine/comm_skeletons/comm.py. Currently this communication is based on MQTT but this could be changed.

All modules of six that run locally are connected by the Spine. This manages the processes for modules and terminates them in an orderly fashion.

## Modules
There are internal and external modules. Internal modules are written in python and are run in a multiprocessing Process. External modules are arbitrary executables that are run using the python subprocess module.

## Todo
- [x] Create Probabalistic Intent Parser based on InferSent and a vector space KNN Classifier
- [x] Create a deterministic Intent parser using regex.
- [ ] add a dialog manager, to manage responses
- [x] allow user input through a chat box
- [ ] create a TTS module
- [ ] create ASR 