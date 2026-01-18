import sqlite3

def init_db():
    conn = sqlite3.connect('library_system.db')
    cursor = conn.cursor()
    # Create a table for transactions if it doesn't exist (Read/Create)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            loan_type TEXT,
            amount REAL,
            status TEXT
        )
    ''')
    conn.commit()
    return conn

def bank_menu():
    conn = init_db()
    
    # [span_4](start_span)Counter-loop requirement: Tracking number of operations in this session[span_4](end_span)
    operation_count = 0 
    
    while True:
        print("\n=== BANK INTERFACE: INTER-LIBRARY LOAN (ILL) ===")
        print("1. Process New ILL Payment (Create)")
        print("2. View All Transactions (Read)")
        print("3. Update Transaction Status (Update)")
        print("4. Cancel/Delete Transaction (Delete)")
        print("5. View Financial Summary (Calculations)")
        print("6. Exit")
        
        choice = input("Select an option: ")
        operation_count += 1
        
        if choice == '1':
            # [span_5](start_span)CREATE operation[span_5](end_span)
            sid = input("Enter Student ID: ")
            loan_type = input("Enter Loan Type (Local/International): ")
            # [span_6](start_span)Calculation/Formula: Higher fee for international loans[span_6](end_span)
            base_fee = 5.0
            tax_rate = 0.06
            if loan_type.lower() == "international":
                base_fee = 20.0
            
            total_price = base_fee + (base_fee * tax_rate)
            print(f"Total Amount (including 6% tax): ${total_price:.2f}")
            
            conn.execute("INSERT INTO transactions (student_id, loan_type, amount, status) VALUES (?, ?, ?, ?)",
                         (sid, loan_type, total_price, 'Paid'))
            conn.commit()
            print("Payment Successful!")

        elif choice == '2':
            # [span_7](start_span)READ operation[span_7](end_span)
            cursor = conn.execute("SELECT * FROM transactions")
            print("\nID | Student ID | Type | Amount | Status")
            for row in cursor:
                print(f"{row[0]} | {row[1]} | {row[2]} | ${row[3]:.2f} | {row[4]}")

        elif choice == '3':
            # [span_8](start_span)UPDATE operation[span_8](end_span)
            tid = input("Enter Transaction ID to update: ")
            new_status = input("Enter new status (Refunded/Pending): ")
            conn.execute("UPDATE transactions SET status = ? WHERE id = ?", (new_status, tid))
            conn.commit()
            print("Transaction updated.")

        elif choice == '4':
            # [span_9](start_span)DELETE operation[span_9](end_span)
            tid = input("Enter Transaction ID to delete: ")
            conn.execute("DELETE FROM transactions WHERE id = ?", (tid,))
            conn.commit()
            print("Transaction deleted.")

        elif choice == '5':
            # [span_10](start_span)Summation and Average requirement[span_10](end_span)
            cursor = conn.execute("SELECT amount FROM transactions")
            amounts = [row[0] for row in cursor]
            if amounts:
                total = sum(amounts)
                avg = total / len(amounts)
                print(f"\n--- Financial Summary ---")
                print(f"Total Revenue: ${total:.2f}")
                print(f"Average Transaction: ${avg:.2f}")
                print(f"Operations performed this session: {operation_count}")
            else:
                print("No data available.")

        elif choice == '6':
            print(f"Exiting. Total operations performed: {operation_count}")
            conn.close()
            break

if __name__ == "__main__":
    bank_menu()