# Neutron-Unfolding
Python implementations of GRAVEL and MLEM algorithims are available within

Hello, I hope you find the use of these unfolding algorithms painless!

1. I have provided all necessary inputs needed to run an example of each algorithm. Those inputs can be found in the directory, unfolding_inputs.

2. execute.py will import all the inputs, run both algorithms, and plot the unfolded algorithms' solution against the time of flight spectrum 
   I recorded experimentally.

3. A special note about the response_matrix() function, the CSV file I was given had the dimensions (201,1024). After importing the (201,1024)
   matrix I redefine it as the transpose of itself, R = R.T, yielding the correct dimensions (1024,201). I have seen other response matrix CSV
   files and it seems to be common practice to store them in this way. Nevertheless, I wanted to bring attention to it to avoid any chance of 
   accidently taking the tranpose of a response matrix that doesn't need it.

4. Currently, GRAVEL is the top-performer and has been validated against a peer-reviewed GRAVEL algorithm. It also proves to be the more      robust of the algorithms.

My choice: GRAVEL
