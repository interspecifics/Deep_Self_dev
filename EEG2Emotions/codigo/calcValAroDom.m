fs = 64;
labels = {'AF3','T7','Pz','T8','AF4'};

idxAF3 = find(strcmp(labels,'AF3'));
idxT7 = find(strcmp(labels,'T7'));
idxPz = find(strcmp(labels,'Pz'));
idxT8 = find(strcmp(labels,'T8'));
idxAF4 = find(strcmp(labels,'AF4'));

samples = size(eegCAR,1);
channels = size(eegCAR,2);
segs = 2;

%--------------------------------------------
pAlpha = zeros(round(samples/(fs*segs)),channels);
pBeta = zeros(round(samples/(fs*segs)),channels);

for c = 1:channels
    startN = 1;
    endN = fs*segs;
    x = 1;
    for v = 1:fs*segs:samples      
       if endN < samples 
           pAlpha(x,c) = bandpower(eegCAR(startN:endN,c),64,[8 13]);
           pBeta(x,c) = bandpower(eegCAR(startN:endN,c),64,[13 30]);
           x = x+1;
           startN = endN;
           endN = startN + (fs*segs);       
       end
    end
end

%--- calc emtoion
valence = pAlpha(:,idxAF4)./ pBeta(:,idxAF4) - pAlpha(:,idxAF3) ./ pBeta(:,idxAF3);
arousal = (pAlpha(:,idxAF3) + pAlpha(:,idxAF4)) ./ (pBeta(:,idxAF3) + pBeta(:,idxAF4));
dominance = pBeta(:,idxT8) ./ pAlpha(:,idxT8) + pBeta(:,idxAF4) ./ pAlpha(:,idxAF4) + pBeta(:,idxPz) ./ pAlpha(:,idxPz);

%-- normalization
valence = (valence - min(valence)) ./ (max(valence) - min(valence));
arousal = (arousal - min(arousal)) ./ (max(arousal) - min(arousal));
dominance = (dominance - min(dominance)) ./ (max(dominance) - min(dominance));

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
    [output, IRR, ORR, ARR] = evalfis([arousal(o) valence(o) dominance(o)], fis);
    
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
outputIdx = [1 2 3 4 6 7 8 9 10];
outputEmotions = emotions_labels(outputIdx);
% ---------------------------------

outputMatrix = zeros(ceil(samples/(fs*segs)), 2+size(outputEmotions,2));
outputMatrix(:,1) = 1:(fs*segs):samples;
outputMatrix(:,2) = (fs*segs):(fs*segs):samples+(fs*segs);
lastSample = outputMatrix(size(outputMatrix,1), 2);
outputMatrix(size(outputMatrix,1), 2) = lastSample - (lastSample - samples);
outputMatrix(1:size(emotionResult,1), 3:2+size(outputIdx,2)) = emotionResult(:,outputIdx);

csvHeaders = ['Start' 'End' outputEmotions];
ot = array2table(outputMatrix);
ot.Properties.VariableNames(:) = csvHeaders;
writetable(ot, [file '_Outputs.csv'])
%csvwrite([file '_Outputs.csv'], [csvHeaders; outputMatrix]);

xx = ((1:1:size(emotionResult,1))./30);
plot(xx, emotionResult(:,outputIdx),'DisplayName','emotionsOut');
title(['Emotions - ' strrep( file , '_' , '') ])
xlabel('Time')
ylabel('Ratio')
legend(outputEmotions);
