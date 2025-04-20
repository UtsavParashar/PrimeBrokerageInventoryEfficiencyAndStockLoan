
`BASEPATH  setenv "C:\\Users\\Utsav\\Desktop\\repos\\PrimeBrokerageInventoryEfficiencyAndStockLoan";

// Stock Loan table
n:100;
tradeDate: asc n?2025.04.01 + til 10;
securityId: `g#n?`goog`amzn`meta;
counterPartyId: n?`jpmc`gs;
quantityReturned: n?1000;
quantityBorrowed: quantityReturned+n?1000;
loanFee: n?5.;
borrowFee: n?5.;
rebateRate: n?2.;

.pb.stockLoanData: ([]
    tradeDate: tradeDate;
    securityId: securityId;
    counterPartyId: counterPartyId;
    quantityReturned: quantityReturned;
    quantityBorrowed: quantityBorrowed;
    loanFee: loanFee;
    borrowFee: borrowFee;
    rebateRate: rebateRate
 );


// Inventory Data
n:100;
tradeDate: asc n?2025.04.01 + til 10;
securityId: `g#n?`goog`amzn`meta;
quantityAvailable: n?1000;
marketPrice: n?100.;

.pb.inventoryData:([]
    tradeDate: tradeDate;
    securityId: securityId;
    quantityAvailable: quantityAvailable;
    marketPrice:marketPrice
 );

update marketPrice+0^(`amzn`meta!100 1000)securityId from `.pb.inventoryData;

//Write CSV in kdb
.pb.util.writeCSV:{[tab; csvFileName]hsym[`$getenv[`BASEPATH],"\\data\\",csvFileName] 0: csv 0: tab};
.pb.util.writeCSV[.pb.inventoryData; "inventory_data.csv"];
.pb.util.writeCSV[.pb.stockLoanData; "stock_loan_data.csv"];
