/*
We can create a program to sort array elements using bubble sort. Bubble sort is one of the simplest sorting algorithm.

In there algorithm, array is traversed from first element to last element. 

Here, current element is compared with the next element and so on. 

If current element is greater than the next element, it is swapped using the "bubbleSort" function.
*/
import java.io.*;
class BubbleSort{
	static void bubbleSort(int[] arr){
		int n = arr.length;
		int temp = 0;
		for(int i=0;i<n;i++){
			for(int j=i;j<n;j++){
				if(arr[i] > arr[j]){
					temp = arr[i];
					arr[i] = arr[j];
					arr[j] = temp;
				}				
			}			
		}
	}
	
	public static void main(String args[]){
		int n = 0;
		System.out.println("Enter how many numbers to sort : ");
		BufferedReader bfr = new BufferedReader(new InputStreamReader(System.in));
		try{
			n = Integer.parseInt(bfr.readLine());
		}
	    catch (IOException err) {
	    	System.out.println("Error input");
	    }
    	
		int[] arr = new int[n];
		for(int i=0;i<n;i++){
			System.out.print("Enter Input : "+(i+1));
			try{
				String inpt = bfr.readLine();
				arr[i] = Integer.parseInt(inpt);
			}
		    catch (IOException err) {
		    	System.out.println("Error input");
		    }
		}
		System.out.println("Before sort : ");
		for(int k=0;k<n;k++){
			System.out.print(arr[k] + " ");
		}
		bubbleSort(arr);
		System.out.println("");
		System.out.println("After sort : ");
		for(int i=0;i<n;i++){
			System.out.print(arr[i] + " ");
		}

	}
	
}

