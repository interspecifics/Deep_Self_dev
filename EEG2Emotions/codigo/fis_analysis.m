n = 216;
samples = n;
% [valence,arousal,dominance] = ndgrid(0:0.01:1,0:0.01:1,0:0.01:1);

valence = zeros(216,1);
arousal = zeros(216,1);
dominance = zeros(216,1);

index = 1;
for i=[0 0.2 0.4 0.6 0.8 1]
    for j=[0 0.2 0.4 0.6 0.8 1]
        for k=[0 0.2 0.4 0.6 0.8 1]
            valence(index) = i;
            arousal(index) = j;
            dominance(index) = k;
            index = index + 1;
        end
    end
end

% valence = reshape(linspace(0,1,length(valence)),216,1);
% arousal = reshape(linspace(0,1,length(valence)),216,1);
% dominance = reshape(linspace(0,1,length(valence)),216,1);


% ------ FIS -----------
emotions_labels = {'BoredSleepy','Contempt','Sadness','Joy','RelaxNeutral','Love','Anger','TenseStress','Fear','Surprise'};
fis = readfis('emotionalEEGFIS2.fis');

emotionRules = 27;
emotionNum = 10;
outputFis = zeros(size(valence,1), emotionRules);
outputFis_i = zeros(1, emotionRules);
emotionResult = zeros(size(valence,1), emotionNum);

o=31;
for o=1:size(valence,1)
    [output, IRR, ORR, ARR] = evalfis(fis, [arousal(o) valence(o) dominance(o)])
    
    for oor_rules = 1: emotionRules
        outputFis_i(1, oor_rules) = max(ORR(:, oor_rules));
    end
    
    outputFis(o, :) = outputFis_i;
end

for ofis=1: size(outputFis,1)
    sumBored = sum( outputFis(ofis,[1 2]) );
    sumContempt = sum( outputFis(ofis,[3 12]) );
    sumSadness = sum( outputFis(ofis,[10 11]) );
    sumJoy = sum( outputFis(ofis,[9 18]) );
    sumRelaxNeutral = sum( outputFis(ofis,[4 5 6 7 8 13 14 15 17]) );
    sumLove = sum( outputFis(ofis,[16 25]) );
    sumAnger = sum( outputFis(ofis,[19 20]) );
    sumTenseStress = sum( outputFis(ofis,[21 24]) );
    sumFear = sum( outputFis(ofis,[22 23]) );
    sumSurprise = sum( outputFis(ofis,[26 27]) );
    if sumSurprise > 0
        emotionResult(ofis,10) = sumSurprise;
    end
    if sumFear > 0
        emotionResult(ofis,9) = sumFear;
    end
    if sumTenseStress > 0
        emotionResult(ofis,8) = sumTenseStress;
    end
    if sumAnger > 0
        emotionResult(ofis,7) = sumAnger;
    end
    if sumLove > 0
        emotionResult(ofis,6) = sumLove;
    end
    if sumRelaxNeutral > 0
        emotionResult(ofis,5) = sumRelaxNeutral;
    end
    if sumJoy > 0
        emotionResult(ofis,4) = sumJoy;
    end
    if sumSadness > 0
        emotionResult(ofis,3) = sumSadness;
    end
    if sumContempt > 0
        emotionResult(ofis,2) = sumContempt;
    end
    if sumBored > 0
        emotionResult(ofis,1) = sumBored;
    end
end

% Select columns to output
outputIdx = [1 2 3 4 5 6 7 8 9 10];
outputEmotions = emotions_labels(outputIdx);
% ---------------------------------

outputMatrix = zeros(n, 3 + size(outputEmotions,2));

outputMatrix(:,1) = [valence];
outputMatrix(:,2) = [arousal];
outputMatrix(:,3) = [dominance];

lastSample = outputMatrix(size(outputMatrix,1), 2);
outputMatrix(size(outputMatrix,1), 2) = lastSample - (lastSample - samples);
outputMatrix(1:n, 3+1:3+size(outputIdx,2)) = emotionResult(:,outputIdx);

csvHeaders = ['valence' 'arousal' 'dominance' outputEmotions];
ot = array2table(outputMatrix);
ot.Properties.VariableNames(:) = csvHeaders;
writetable(ot, strcat('centroid_test', '_Outputs.csv'))
