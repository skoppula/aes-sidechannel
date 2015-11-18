import processing.serial.*;
import java.io.*;
int mySwitch=0;
int counter=0;
String [][] lines;
Serial myPort;


void setup(){
 myPort = new Serial(this, "/dev/cu.usbmodem1411", 9600);
 myPort.bufferUntil('\n');
 System.out.println(myPort);
 lines = new String[2][16];
}

void draw() {
 readData("/Users/hol/junior/6.UAR/DPA Analysis/858_side_channel_code/aes-sidechannel/myPlaintextData.txt");
 System.out.println(lines[0][0]);
 for(int i = 0; i < lines.length; i++) {
   for(int j = 0; j < lines[i].length; j++) {
     myPort.write(lines[i][j]);
   }
   delay(3000);
 }
}


/* The following function will read from a CSV or TXT file */
void readData(String myFileName){
 
 File file=new File(myFileName);
 BufferedReader br=null;
 
 try{
   br=new BufferedReader(new FileReader(file));
   String text=null;
   int lineno = 0;
   
   while((text=br.readLine())!=null){
     /* Spilt each line up into bits and pieces using a comma as a separator */
     String[] line_parts = splitTokens(text,",");
     for(int i =0; i < line_parts.length; i++) {
       lines[lineno][i] = line_parts[i];
     }
     lineno += 1;
   }
 }catch(FileNotFoundException e){
   e.printStackTrace();
 }catch(IOException e){
   e.printStackTrace();
 }finally{
   try {
     if (br != null){
       br.close();
     }
   } catch (IOException e) {
     e.printStackTrace();
   }
 }
}