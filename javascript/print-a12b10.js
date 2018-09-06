var x = 'a12b10';
var ary = [];

var count = 0;
var pr = 0;
for(i=0;i<x.length;i++){
	
	if(x[i] >= 0){
		if(pr == 1){
			count--;
		}
		pr = 1;
		ary[count] = ''+ (ary[count]?ary[count]:'') + x[i];
	}else{
		pr = 0;
		ary[count] = x[i];
	}
	count++;

}
console.log(ary);
var res = '';
for(i=0;i<ary.length;i++){
	for(j=i+1;j<ary[i+1];j++){
		res = res + ary[i];
	}
	i++;
}
console.log(res);
