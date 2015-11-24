import processing.serial.*;
import java.io.*;
int mySwitch=0;
int counter=0;
int LINES_COUNT = 500;
char [][] lines = new char[LINES_COUNT][16];
Serial myPort;

void setup(){
 myPort = new Serial(this, "COM3", 9600);
 myPort.bufferUntil('\n');
 readData("F:/Academics/[ MIT ]/6.858 - Computer Systems Security/Final Project/sidechannel-repo/myPlaintextData.txt");
 delay(1000);
 for(int j=0; j < lines[0].length; j++) {
   myPort.write(lines[0][j]);
 }
 delay(1000);
 for(int i = 0; i < lines.length; i++) {
   System.out.print("Sent plaintext: ");
   for(int j = 0; j < lines[i].length; j++) {
     System.out.print(lines[i][j]);
     myPort.write(lines[i][j]);
   }
 System.out.println();
 delay(5000);
 }
}

void draw() {}

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
     String[] line_parts = splitTokens(text,", ");
     for(int i =0; i < line_parts.length; i++) {
       lines[lineno][i] = (char) Integer.parseInt(line_parts[i]);
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

void serialEvent (Serial myPort) {
 // get the ASCII string:
 String inString = myPort.readStringUntil('\n');

 if (inString != null) {
   // trim off any whitespace:
   inString = trim(inString);
   System.out.println("\t" + inString);
 }
 
}