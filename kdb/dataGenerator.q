
// Stock Loan table
n:100;
loanDate: asc n?2025.04.01 + til 10;
securityId: `g#n?`goog`amzn`meta;
counterPartyId: n?`jpmc`gs;
quantityReturned: n?1000;
quantityBorrowed: quantityReturned+n?1000;
loanFee: n?5.;
borrowFee: n?5.;
rebateRate: n?2.;

.pb.stockLoanData: ([]
    loanDate: loanDate;
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

update marketPrice: 100+marketPrice from .pb.inventoryData where sym=`goog;
update marketPrice: 1000+marketPrice from .pb.inventoryData where sym=`meta;