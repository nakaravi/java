
import java.io.*;

class triangle{
	public static void main(String args[]){
		int rows=0, i, j;
		
		
		InputStreamReader istream = new InputStreamReader(System.in) ;
		BufferedReader bufRead = new BufferedReader(istream);
		try {
			System.out.println("Enter number of rows : ");
            String row = bufRead.readLine();
            rows = Integer.parseInt(row);
       }
       catch (IOException err) {
            System.out.println("Error reading line");
       }
		
		

		for(i=1;i<=rows;i++){
			for(j=1;j<=i;j++){
				System.out.print(j + " ");
			}
			System.out.println("");
		}
	}
}
