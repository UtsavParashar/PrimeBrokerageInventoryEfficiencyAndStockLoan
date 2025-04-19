/l getevn[`BASEPATH],"\\kdb\\qLoader.q";

//Stock Loan Analysis
// Utilization Percentage
// Formula - Utilization Percentage = 100 * outstandingQuantityBorrowed % quantityAvailable 
// Formula - outstandingQuantityBorrowed = sum[quantityBorrowed] - sum quantityReturned
// quantityAvailable comes from inventoryData

select outstandingQuantityBorrowed: quantityBorrowed-quantityReturned by loanDate, securityId from .pb.stockLoadData