/*extends one class from other class*/
class Main{
	float salary=50000;
}
class extendsClass extends Main{
	int bonus=1000;
	
	public static void main(String args[])
	{
		extendsClass ec = new extendsClass();
		System.out.println("Salary : " + ec.salary);
		System.out.println("Bonus  : " + ec.bonus);
	}
}
