// Load the data from CSV for now
// TODO - Enhancement -- Have TP, RDB and HDB for real time inventory analysis

`BASEPATH  setenv "C:\\Users\\Utsav\\Desktop\\repos\\PrimeBrokerageInventoryEfficiencyAndStockLoan";

.pb.inventoryData: ("DSSJFS"; enlist csv) 0: hsym `$getenv[`BASEPATH],"\\data\\inventory_data.csv";
.pb.stockLoanData: ("DSSJJFFF"; enlist csv) 0: hsym `$getenv[`BASEPATH],"\\data\\stock_loan_data.csv";


