# Neutron-Unfolding
Python implementations of GRAVEL and MLEM algorithims are available within

Hello, I hope you find the use of these unfolding algorithms painless!

1. I have provided all necessary inputs needed to run an example of each algorithm. Those inputs can be found in the directory, unfolding_inputs.

2. execute.py will import all the inputs, run both algorithms, and plot the unfolded algorithms' solution against the time of flight spectrum 
   I recorded experimentally. The execute does require one input, this is which intitial guess it to be used; constant or ToF.

3. A special note about the response_matrix() function, the CSV file I was given had the dimensions (201,1024). After importing the (201,1024)
   matrix I redefine it as the transpose of itself, R = R.T, yielding the correct dimensions (1024,201). I have seen other response matrix CSV
   files and it seems to be common practice to store them in this way. Nevertheless, I wanted to bring attention to it to avoid any chance of 
   accidently taking the tranpose of a response matrix that doesn't need it.

4. execute.py was setup to run both algorithms for comparison purposes. Because GRAVEL was the top performing algorithm, I'd suggest using it over MLEM. The script       execute_gravel.py will use only GRAVEL

5. In the report_and_presentation directory are a copy of the lab report and project presentation that went into developing these algorithms 
