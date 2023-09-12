function initialize(){
    inputContainer = document.getElementById("inputform"); 
    diceTablew = document.getElementById("dicetable"); 
    diceNumw = document.getElementById("howManyDice"); 
    diceTimesw = document.getElementById("howManyTimes"); 
      
    mean_ = document.getElementById("mean"); 
    median_ = document.getElementById("median"); 
    mode_ = document.getElementById("mode"); 

    numDoubles_ = document.getElementById("numOfDoubles"); 
    numTriples_ = document.getElementById("numOfTriples"); 

    numDice = ""; 
    numTimes = ""; 
        
    rollDice(); 
}

function clearTable(){
    let rowCount = diceTablew.rows.length;
    let tableHeaderCount = 1; // starting from roll 1's row 
    let k = 1;
    for (let j = tableHeaderCount; j < rowCount; j++) {
      diceTablew.deleteRow(tableHeaderCount);
    }
    let i = 1; // corresponds with roll 1's row 
    while(i <= numDice){ // checking with the total number of dice 
      firstrow.deleteCell(1);
      i++;
    }      
}
    
function rollDice(){
    var numRolls = parseInt(inputContainer.rollTimes.value); 
    numDice = parseInt(inputContainer.dices.value); 
    
    makeColumn(numDice); 
    
    var sum = 0; 
    var numVals = 0; 
    
    numOfDoubles_ = 0; 
    numOfTriples_ = 0; 
    
    listOfValues = []; 
    
    for (var i = 0; i < numRolls; i++) {
        dieRoll1 = getRandomInteger(1,6); 
        listOfValues.push(dieRoll1); 
    
        var newRow = diceTablew.insertRow();
        var newCell = newRow.insertCell();
        newCell.innerHTML = "Roll " + (i+1);
    
        newCell = newRow.insertCell(); 
        newCell.innerHTML = dieRoll1; 
    
        if (numDice >= 2) {
            dieRoll2 = getRandomInteger(1,6); 
            listOfValues.push(dieRoll2); 
            
            newCell = newRow.insertCell(); 
            newCell.innerHTML = dieRoll2; 
    
            if (dieRoll1 == dieRoll2) {
                numOfDoubles_++; 
            }
        }
    
        if (numDice == 3) {
            dieRoll3 = getRandomInteger(1,6); 
            listOfValues.push(dieRoll3); 
            
            newCell = newRow.insertCell(); 
            newCell.innerHTML = dieRoll3; 
    
            if (dieRoll1 == dieRoll2) {
                numOfDoubles_++; 
                if (dieRoll2 == dieRoll3) {
                    numOfTriples_++; 
                }
            }
    
            if (dieRoll1 == dieRoll3) {
                numOfDoubles_++; 
                if (dieRoll2 == dieRoll1) {
                    numOfTriples_++; 
                }
            }
            
            if (dieRoll2 == dieRoll3) {
                numOfDoubles_++; 
                if (dieRoll1 == dieRoll2) {
                    numOfTriples++; 
                }
            }
        }
    }
    
        display(); 
}

function numDoubles() {
    return numOfDoubles_; 
}

function numTriples() {
    return numOfTriples_; 
}

          let getRandomInteger = (min, max) => parseInt(Math.random() * max - (min - 1) + min); 

          function makeColumn(num) {
              for (let i = 1; i <= num; i++) {
                  var newCol = document.getElementById("firstrow").insertCell(); 
                  newCol.innerHTML = "Dice" + i + "Result"; 
              }
          }

        function calculateMedian(values) {
            let median = 0; 
            values.sort((a, b) => a-b); // sorts in increasing/ascending order 
            if (values.length % 2 === 0) { // check if length is even 
                median = (values[values.length / 2 - 1] + values[values.length / 2]) / 2; 
            } else { // length is odd 
                median = values[(values.length - 1) / 2]; 
            }
            return median; 
        }

          function calculateMean() {
              totalSum = 0; 
              totalNum = 0; 
              for (let j = 0; j < listOfValues.length; j++) {
                  totalSum = listOfValues[j]; 
                  totalNum++; 
              }
              return Math.round(100 * (totalSum / totalNum)) / 100; 
          }

        function calculateMode(values) {
            let maxVal = 0; 
            let maxCount = 0; 
            for (let i = 0; i < values.length; i++) { // a nested loop 
                let count = 0; 
                for (let j = 0; j < values.length; j++) { // compares every value in column 
                    if (values[j] === values[i]) {
                        count++; 
                    }
                }
                if (count > maxCount) {
                maxCount = count; 
                maxVal = values[maxCount]; 
                }
            }

            return maxVal; 
        }

          function display() {
              medianCalc = calculateMedian(listOfValues); 
              median_.innerHTML = medianCalc; 

              meanCalc = calculateMean(); 
              mean_.innerHTML = meanCalc; 

              modeCalc = calculateMode(listOfValues); 
              mode_.innerHTML = modeCalc; 

              doublesCalc = numDoubles(); 
              numDoubles_.innerHTML = doublesCalc; 

              triplesCalc = numTriples(); 
              numTriples_.innerHTML = triplesCalc; 
          }