import numpy as np

driftData = {}

if driftData['auto_man'] == 1:
    if driftData['verstasjon']['wind'] > 10:
        g = 10
        #sett minste mulige steg
    else:
        rh = driftData['verstasjon']['hum']         #finner wetbulb     NB! må testes       PS: kan sikkert settes i en funksjon        PSS: Burde settes i en funksjon for lesbarhetens skyld
        tdb = driftData['verstasjon']['temp_2']
        mbpressure = driftData['verstasjon']['press']

        es = 6.112 * np.exp((17.67 * tdb) / (tdb + 243.5))
        e = es * (rh / 100)

        edifference = 1
        previousign = 1
        incr = 10
        twguess = 0

        dewpoint = 243.5 * np.log((e) / (6.112)) / (17.67 - np.log((e / 6.112))) 

        while (np.abs(edifference) > 0.005):
            ewguess = 6.112 * np.exp((17.67 * twguess) / (twguess + 243.5)) 
            eguess = ewguess - mbpressure * (tdb - twguess) * 0.00066 * (1 + (0.00115 * twguess)) 
            edifference = e - eguess 

            if (edifference == 0):
                break 
        
            else:
                if (edifference < 0):
                    cursign = -1 

                    if (cursign != previousign):
                        previousign = cursign 
                        incr = incr / 10 
               
                    else:
                        incr = incr 
                
                else:
                    cursign = 1 

                    if (cursign != previousign):
                        previousign = cursign 
                        incr = incr / 10 
                
                    else:
                        incr = incr 
        
            twguess = twguess + incr * previousign 

        twb = np.round(twguess * 100) / 100

        wetBulb = twb

        if wetBulb < -7:
            steg = max()
        elif wetBulb < -3:
            steg = min()

        

else:
    #set man steg



    
