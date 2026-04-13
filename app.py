from flask import Flask, render_template, request, redirect

app = Flask(__name__)

expenses = []

@app.route('/')
def index():
    balances = {}

    for e in expenses:
        total = e['amount']
        members = e['members']
        paid_dict = e['paid_by']

        share = total // len(members)

        # initialize
        for m in members:
            balances[m] = balances.get(m, 0)

        # subtract share
        for m in members:
            balances[m] -= share

        # add payments
        for person, amt in paid_dict.items():
            balances[person] = balances.get(person, 0) + amt

    # settlement
    owes = []
    gets = []

    for person, amount in balances.items():
        if amount < 0:
            owes.append([person, -amount])
        elif amount > 0:
            gets.append([person, amount])

    transactions = []

    i, j = 0, 0
    while i < len(owes) and j < len(gets):
        payer, owe_amt = owes[i]
        receiver, get_amt = gets[j]

        pay = min(owe_amt, get_amt)

        transactions.append(f"{payer} pays ₹{pay} to {receiver}")

        owes[i][1] -= pay
        gets[j][1] -= pay

        if owes[i][1] == 0:
            i += 1
        if gets[j][1] == 0:
            j += 1

    return render_template('index.html',
                           expenses=expenses,
                           balances=balances,
                           transactions=transactions)


@app.route('/add', methods=['POST'])
def add():
    name = request.form.get('name')
    amount = request.form.get('amount')
    paid_by = request.form.get('paid_by')
    paid_amounts = request.form.get('paid_amounts')
    members = request.form.get('members')

    if not name or not amount or not paid_by or not paid_amounts or not members:
        return "Error: Fill all fields"

    amount = int(amount)

    # convert inputs
    people = [p.strip() for p in paid_by.split(',')]
    amounts = [int(a.strip()) for a in paid_amounts.split(',')]

    if len(people) != len(amounts):
        return "Error: Paid names and amounts mismatch"

    paid_dict = {}
    for i in range(len(people)):
        paid_dict[people[i]] = amounts[i]

    members_list = [m.strip() for m in members.split(',') if m.strip()]

    expenses.append({
        'name': name,
        'amount': amount,
        'paid_by': paid_dict,
        'members': members_list
    })

    return redirect('/')


@app.route('/reset')
def reset():
    global expenses
    expenses = []
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)