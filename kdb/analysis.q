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
.pb.mergedData: (select totalQtyAvai: sum quantityAvailable, wavgMktPx: quantityAvailable wavg marketPrice by tradeDate, securityId from .pb.inventoryData) 
    lj select outstandingQtyBorrowed: 0^(sum[quantityBorrowed]-sum[quantityReturned]) by tradeDate, securityId from .pb.stockLoanData;

update utilizationPercentage:100 * (outstandingQtyBorrowed % totalQtyAvai) from  .pb.mergedData;

t:([] dt:2025.04.04 2025.04.04 2025.04.04 2025.04.04 2025.04.05 2025.04.05 2025.04.05 2025.04.05 2025.04.05;
    ratings: `AAA`BBB`AAA`BBB`AAA`BBB`BBB`AAA`AAA;
    side: `B`S`S`B`S`B`S`B`S;
    notional:10*1+til 9
 );

/t: select from t where dt=2025.04.05;

.up.tab:select sum notional by dt, ratings, side from t;
.up.ratings:asc exec distinct side from .up.tab;
.up.pvt:0!exec .up.ratings#(side!notional) by ratings:ratings from .up.tab;
select ratings, buySellRatio:B%S  from .up.pvt

([] dt:(2#2025.04.04), 2#2025.04.05),'(.up.res1, .up.res2)

60%70