 %%CAR Common Average Reference

function [senalFiltrada]= applyCAR(senal)

[muestras,canales]=size(senal);
senalFiltrada=zeros(muestras,canales);

for i=1:muestras
    for  j=1:canales
        senalFiltrada(i,j)=senal(i,j)-mean(senal(i,:));               
    end
end

end