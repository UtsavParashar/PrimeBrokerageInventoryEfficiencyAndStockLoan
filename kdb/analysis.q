`BASEPATH  setenv "C:\\Users\\Utsav\\Desktop\\repos\\PrimeBrokerageInventoryEfficiencyAndStockLoan";
// \l getevn[`BASEPATH],"\\kdb\\qLoader.q";
// \l getevn[`BASEPATH],"\\kdb\\dataGenerator.q";


//Load Data From CSV
.pb.utils.loadCSV: {[dataTypes; csvFileName] (dataTypes; enlist csv) 0: hsym `$getenv[`BASEPATH],"\\data\\",csvFileName};
.pb.stockLoanData: .pb.utils.loadCSV["DSSFJFFF"; "stock_loan_data.csv"];
.pb.inventoryData: .pb.utils.loadCSV["DSJF"; "inventory_data.csv"];


// Stock Loan Analysis
// Utilization Percentage
// Formula - Utilization Percentage = 100 * outstandingQuantityBorrowed % quantityAvailable 
// Formula - outstandingQuantityBorrowed = sum[quantityBorrowed] - sum quantityReturned
// quantityAvailable comes from inventoryData
.pb.mergedData: 0^(select totalQtyAvai: sum quantityAvailable, wavgMktPx: quantityAvailable wavg marketPrice, sum quantityAvailable by tradeDate, securityId from .pb.inventoryData) 
    lj select outstandingQtyBorrowed: (sum[quantityBorrowed]-sum[quantityReturned]), wtAvgLoanFee: quantityBorrowed wavg loanFee, wtAvgRebateRate: quantityBorrowed wavg rebateRate by tradeDate, securityId from .pb.stockLoanData;

update utilizationPercentage:100 * (outstandingQtyBorrowed % totalQtyAvai),
       dailyImpact: (outstandingQtyBorrowed*wavgMktPx*wtAvgLoanFee)%360,
       opportunityCost: (quantityAvailable - outstandingQtyBorrowed)*wavgMktPx*wtAvgRebateRate%360,
       demandRatio: outstandingQtyBorrowed%quantityAvailable
    from  .pb.mergedData;






