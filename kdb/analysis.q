/l getevn[`BASEPATH],"\\kdb\\qLoader.q";
// /l getevn[`BASEPATH],"\\kdb\\dataGenerator.q";


//Load Data From CSV
.pb.utils.loadCSV: {[dataTypes; csvFileName] (dataTypes; enlist csv) 0: hsym `$getenv[`BASEPATH],"\\data\\",csvFileName};
.pb.stockLoadData: .pb.utils.loadCSV["DSSFJFFF"; "stock_loan_data.csv"];
.pb.inventoryData: .pb.utils.loadCSV["DSJF"; "inventory_data.csv"];


// Stock Loan Analysis
// Utilization Percentage
// Formula - Utilization Percentage = 100 * outstandingQuantityBorrowed % quantityAvailable 
// Formula - outstandingQuantityBorrowed = sum[quantityBorrowed] - sum quantityReturned
// quantityAvailable comes from inventoryData
.pb.mergedData: .pb.inventoryData lj 2!update outstandingQtyBorrowed: sum[quantityBorrowed]- sum quantityReturned by tradeDate, securityId from .pb.stockLoanData;

update utilizationPercentage:100 * (outstandingQtyBorrowed % quantityAvailable) from  .pb.mergedData;