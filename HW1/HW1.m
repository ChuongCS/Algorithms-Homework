
A=[1 5 3 -8 9 4];
B=[0 -1 6 2 3 10];
Asort=sort(A);
Bsort=sort(B);
i=1;j=1;
count=0;
while(i<=length(Asort)&& j<=length(Bsort))
    if(Asort(i)==Bsort(j))
        i=i+1;
        j=j+1; 
        count=count+1;
        break
    else if (Asort(i)>Bsort(j))
        j=j+1;
    else
        i=i+1;
    end
    end
end
if count==0
    fprintf('there is no common elements');
else 
    fprintf('there exists at least one common element');
end

