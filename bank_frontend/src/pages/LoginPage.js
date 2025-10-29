import React, { useState } from "react";
import { loginUser } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(form);
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      alert("Login failed");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl mb-4">Bank Login</h1>
      <form onSubmit={handleSubmit} className="flex flex-col w-64">
        <input name="username" placeholder="Username" onChange={handleChange} className="mb-2 p-2 border rounded" />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} className="mb-2 p-2 border rounded" />
        <button className="p-2 bg-blue-500 text-white rounded">Login</button>
      </form>
      <p className="mt-2 text-blue-600 cursor-pointer" onClick={() => navigate("/register")}>
        Register here
      </p>
    </div>
  );
}