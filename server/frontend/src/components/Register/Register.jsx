import React, { useState } from "react";

const Register = () => {
    const [userName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");

    const register = async (e) => {
        e.preventDefault();
        const register_url = window.location.origin + "/djangoapp/register";
        const res = await fetch(register_url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                userName, password, firstName, lastName, email
            }),
        });
        const json = await res.json();
        if (json.status) {
            sessionStorage.setItem('username', json.userName);
            window.location.href = window.location.origin;
        } else if (json.error === "Already Registered") {
            alert("Username already exists.");
        }
    };

    return (
        <div>
            <h2>Sign Up</h2>
            <form onSubmit={register}>
                <input type="text" placeholder="Username" value={userName} onChange={e => setUserName(e.target.value)} required /><br/>
                <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required /><br/>
                <input type="text" placeholder="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} required /><br/>
                <input type="text" placeholder="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} required /><br/>
                <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required /><br/>
                <button type="submit">Register</button>
            </form>
        </div>
    );
};

export default Register;