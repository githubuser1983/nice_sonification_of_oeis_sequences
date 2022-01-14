Nice sonification of OEIS sequences:

To sonify a sequence, first copy from configurations a yaml file you like.
Then change:

   the name of the file
   
   the name of the midi-file
   
   the sequence (which you can copy and paste from the corresponding OEIS-page)

You can also change the start note, etc.

Then start the sonification by:

sage number_sequence_sonification.py configurations/A307984.yaml

This will produce a midi-file in the folder ./midi/
The name of the midi file can be specified in the yaml file.
