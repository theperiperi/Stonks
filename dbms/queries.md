### DBMS Queries

1. Select all users
   ```sql
   SELECT * FROM users;
   ```

2. Select all methods
   ```sql
   SELECT * FROM methods;
   ```

3. Select all transactions
   ```sql
   SELECT * FROM transactions;
   ```

4. Update user password
   ```sql
   UPDATE users SET password = 'new_password' WHERE userid = 1;
   ```

5. Delete transaction
   ```sql
   DELETE FROM transactions WHERE transactionid = 1;
   ```

6. Select users with password containing 'abc'
   ```sql
   SELECT * FROM users WHERE password LIKE '%abc%';
   ```

7. Select transactions with amount greater than 50
   ```sql
   SELECT * FROM transactions WHERE amount > 50;
   ```

8. Select users with transactions using Cash method
   ```sql
   SELECT * FROM users WHERE userid IN (SELECT userid FROM transactions WHERE methodid = (SELECT methodid FROM methods WHERE method_name = 'Cash'));
   ```

9. Select methods used by user with userid = 1
   ```sql
   SELECT * FROM methods WHERE methodid IN (SELECT methodid FROM transactions WHERE userid = 1);
   ```

10. Calculate total transaction amount
    ```sql
    SELECT SUM(amount) AS total_amount FROM transactions;
    ```

11. Calculate average transaction amount
    ```sql
    SELECT AVG(amount) AS average_amount FROM transactions;
    ```

12. Find latest transaction timestamp
    ```sql
    SELECT MAX(timestamp) AS latest_transaction FROM transactions;
    ```

13. Count total number of users
    ```sql
    SELECT COUNT(*) AS user_count FROM users;
    ```

14. Count number of transactions per user
    ```sql
    SELECT userid, COUNT(*) AS transaction_count FROM transactions GROUP BY userid;
    ```

15. Join users and transactions
    ```sql
    SELECT u.userid, u.password, t.transactionid, t.methodid, t.amount FROM users u INNER JOIN transactions t ON u.userid = t.userid;
    ```

16. Select users with no transactions
    ```sql
    SELECT * FROM users WHERE userid NOT IN (SELECT userid FROM transactions);
    ```

17. Select users with transactions using Card method
    ```sql
    SELECT * FROM users WHERE userid IN (SELECT userid FROM transactions WHERE methodid = (SELECT methodid FROM methods WHERE method_name = 'Card'));
    ```

18. Select transactions with amount between 50 and 100
    ```sql
    SELECT * FROM transactions WHERE amount BETWEEN 50 AND 100;
    ```

19. Select users with transactions after '2024-01-01'
    ```sql
    SELECT * FROM users WHERE userid IN (SELECT userid FROM transactions WHERE timestamp > '2024-01-01');
    ```

20. Count transactions per method
    ```sql
    SELECT m.method_name, COUNT(*) AS transaction_count FROM methods m INNER JOIN transactions t ON m.methodid = t.methodid GROUP BY m.methodid;
    ```

21. Calculate average transaction amount per user
    ```sql
    SELECT userid, AVG(amount) AS average_transaction_amount FROM transactions GROUP BY userid;
    ```

22. Calculate total transaction amount per user
    ```sql
    SELECT u.userid, u.password, SUM(t.amount) AS total_transaction_amount FROM users u INNER JOIN transactions t ON u.userid = t.userid GROUP BY u.userid;
    ```

23. Find user with highest total transaction amount
    ```sql
    SELECT u.userid, u.password, SUM(t.amount) AS total_transaction_amount FROM users u INNER JOIN transactions t ON u.userid = t.userid GROUP BY u.userid ORDER BY total_transaction_amount DESC LIMIT 1;
    ```

24. Find method with highest total transaction amount
    ```sql
    SELECT m.method_name, SUM(t.amount) AS total_transaction_amount FROM methods m INNER JOIN transactions t ON m.methodid = t.methodid GROUP BY m.methodid ORDER BY total_transaction_amount DESC LIMIT 1;
    ```

25. Select transactions for user with highest total transaction amount
    ```sql
    SELECT * FROM transactions WHERE userid = ( SELECT u.userid FROM users u INNER JOIN transactions t ON u.userid = t.userid GROUP BY u.userid ORDER BY SUM(t.amount) DESC LIMIT 1 );
    ```

26. Find method with lowest total transaction amount
    ```sql
    SELECT m.method_name, SUM(t.amount) AS total_transaction_amount FROM methods m INNER JOIN transactions t ON m.methodid = t.methodid GROUP BY m.methodid ORDER BY total_transaction_amount ASC LIMIT 1;
    ```

27. Count transactions per user in the last month
    ```sql
    SELECT u.userid, u.password, COUNT(*) AS transaction_count FROM users u INNER JOIN transactions t ON u.userid = t.userid WHERE t.timestamp >= DATE('now', '-1 month') GROUP BY u.userid;
    ```

28. Count transactions per method
    ```sql
    SELECT m.method_name, COUNT(t.transactionid) AS transaction_count FROM methods m LEFT JOIN transactions t ON m.methodid = t.methodid GROUP BY m.methodid;
    ```

29. Select users with transactions in the last 7 days
    ```sql
    SELECT DISTINCT u.userid, u.username FROM users u JOIN transactions t ON u.userid = t.userid WHERE t.timestamp >= DATE('now', '-7 days');
    ```

30. Select users with no transactions
    ```sql
    SELECT * FROM users WHERE userid NOT IN (SELECT DISTINCT userid FROM transactions);
    ```

31. Select users with transactions greater than $200
    ```sql
    SELECT DISTINCT u.userid, u.username FROM users u JOIN transactions t ON u.userid = t.userid WHERE t.amount >
    ```
32. List Transactions Made by Users Whose Passwords Contain 'password':
    ```sql
    SELECT * 
    FROM transactions 
    WHERE userid IN (SELECT userid FROM users WHERE password LIKE '%password%');
    ```
33. List Methods Where the Total Transaction Amount is Greater Than $500:
    ```sql
    SELECT m.method_name 
    FROM methods m 
    JOIN transactions t ON m.methodid = t.methodid 
    GROUP BY m.methodid 
    HAVING SUM(t.amount) > 500;
    ```
34. List Users Who Have Made More Than 3 Transactions:
    ```sql
    SELECT u.userid, u.username 
    FROM users u 
    JOIN transactions t ON u.userid = t.userid 
    GROUP BY u.userid 
    HAVING COUNT(t.transactionid) > 3;
    ```
35. List Users Who Have Made Transactions Using Both Methods:
    ```sql
    SELECT u.userid, u.username 
    FROM users u 
    JOIN transactions t ON u.userid = t.userid 
    GROUP BY u.userid 
    HAVING COUNT(DISTINCT t.methodid) > 1;
    ```
36. List Users and Their Total Transaction Amounts, Sorted in Descending Order of Amount:
    ```sql
    SELECT u.userid, u.username, SUM(t.amount) AS total_amount 
    FROM users u 
    JOIN transactions t ON u.userid = t.userid 
    GROUP BY u.userid 
    ORDER BY total_amount DESC;
    ```
37. List Users Who Have Made Transactions Using Both Cash and GPay:
    ```sql
    SELECT u.userid, u.username 
    FROM users u 
    JOIN transactions t ON u.userid = t.userid 
    GROUP BY u.userid 
    HAVING COUNT(DISTINCT t.methodid) = 2;
    ```