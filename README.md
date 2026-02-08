# Headspace Wanderers
This is the Headspace Wizards repository for UGAHacks11
## Name of Team
~~~
Sankalp Amaravadi
Kahmin Keller
Mathew Martin
Gautham Gadipati
~~~
## Purpose of Project
~~~

~~~
## Tools Used
~~~
Physical Tools
- Whiteboard
- Humor
- Arduino Mega 2560
- DHT11 sensor
Software Tools
- Google Drive products- Google Docs, Google Slides
- Virtual Studio Code
- JetBrains IDEs 
- GitHub
- Arduino IDE

~~~

## Public Frameworks (APIs and similar) Used
~~~
PySerial
~~~
## Challenges Faced
~~~
1) We had a challenge when it came to filtering out main hackathon concepts
~~~
## How The Challenges Were Overcome
~~~
1) We set goals for ourselves to keep both scope creep and nonfeasible goals in check. We understood that there is a total of less than 30 hours for us to build a complete product, so we are taking advantage of all possible resources, including llm access through the hackathon to organize our efforts and deliver a product.

2) The first night, we had settled on a working schedule for the hackathon the subsequent day, providing soft and hard deadlines to prevent us from squandering our time. We decided the entirety of the first night would be utilized to examine as many possibilities and analyze the challenges from Cox and State Farm to create a solution that could scale for community benefit.

3) We found ourselves disagreeing on the nature of the result we are building. The technology itself is capable of performing under multiple circumstances. Finally, we decided to coalesce together for the project to perform within automobiles for the sake of spotting vulnerabilities for water damage, which is a major cause of significant damage if not total loss for vehicles. We are now able to proceed while focusing our effort and improving the use case in which we are ensuring that vehicles are maintaining an optimal performance environment for vehicles after disaster.

4) The team spotted multiple limitations in the arduino kit. There had to be a resolution for the small memory allotment of 256kb of secondary memory as well as inability to connect through wifi. The team tasked itself with running the kit without the above features for a seamless user experience with the sensor kit. Thus, the team decided that the pertinent data had to be saved as csv delimited by comma to optimize for space, and this data would be downloaded to the device to be displayed on the dashboard when connected to a computer. The sensor is then capable of sensor data storage and quick passing for analysis by any user with the program.

5) A major roadblock hit was accessing the data created by the arduino. The task set was to at the very least create capability for the information from the arduino to be exported to a csv file which is easily handled by the python code. The team was capable of employing the Putty program to access the serial port of the arduino runtime. This allowed the team to run the arduino and export the data received through the sensors directly to a csv file. Though, this does not address data accumulation when there is no connection to a computer for this operation, and due to time constraints, this will not be addressed.
1) We set goals for ourselves to keep both scope creep and unrealistic goals in check.  This allowed us to focus on achieving the goals the team set on itself
2) Technology challenges on how we planned to send data over. intially thought bluetooth, thne RFID.
~~~
## Project rules- how the project is to be completed
~~~
While building the hardware, we want to keep the wire colors seperated by what they will be used for.
Green wires are sensor outputs
Red wires are power wires
Black wires are ground wires
Blue wires are control input 
~~~
