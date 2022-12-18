CREATE TABLE expense_tracker_ledger (
    id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
    expense_id int NOT NULL,
    group_id varchar(100) NOT NULL,
    who_paid_id varchar(500) NOT NULL,
    for_whom_id varchar(500) NOT NULL,
    amount double NOT NULL, 
    if_paid ENUM('true','false') default 'false',
    date_created datetime DEFAULT CURRENT_TIMESTAMP
);