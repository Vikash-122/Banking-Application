import React, { useEffect, useState } from "react";
import { getAccounts } from "../api/api";

export default function Dashboard() {
  const [accounts, setAccounts] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem("token");
    getAccounts(token)
      .then((res) => setAccounts(res.data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">My Accounts</h1>
      <ul>
        {accounts.map((acc) => (
          <li key={acc.account_id} className="border p-2 mb-2 rounded">
            <strong>{acc.account_type}</strong> - {acc.account_number} : ₹{acc.balance}
          </li>
        ))}
      </ul>
    </div>
  );
}