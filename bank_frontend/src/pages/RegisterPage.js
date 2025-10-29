import React, { useState } from "react";
import { registerUser } from "../api/api";
import { useNavigate } from "react-router-dom";

export default function RegisterPage() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await registerUser(form);
      alert("Registration successful");
      navigate("/");
    } catch (err) {
      alert("Error registering user");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl mb-4">Register</h1>
      <form onSubmit={handleSubmit} className="flex flex-col w-64">
        <input name="username" placeholder="Username" onChange={handleChange} className="mb-2 p-2 border rounded" />
        <input name="email" placeholder="Email" onChange={handleChange} className="mb-2 p-2 border rounded" />
        <input name="password" type="password" placeholder="Password" onChange={handleChange} className="mb-2 p-2 border rounded" />
        <button className="p-2 bg-green-500 text-white rounded">Register</button>
      </form>
      <p className="mt-2 text-blue-600 cursor-pointer" onClick={() => navigate("/")}>
        Back to Login
      </p>
    </div>
  );
}