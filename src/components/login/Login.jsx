import React, { useState, useEffect } from "react";
import "./login.css";
import { toast } from "react-toastify";
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
} from "firebase/auth";
import { auth, db } from "../../lib/firebase";
import { doc, setDoc } from "firebase/firestore";
import upload from "../../lib/upload";
import countries from "i18n-iso-countries";
import enLocale from "i18n-iso-countries/langs/en.json";

export default function Login() {
  const [avatar, setAvatar] = useState({
    file: null,
    url: "",
  });
  const [loading, setLoading] = useState(false);
  const [selectedCountry, setSelectedCountry] = useState("");
  const [countryOptions, setCountryOptions] = useState({});
  const [isRegistering, setIsRegistering] = useState(false); // Toggle between Sign In and Sign Up

  useEffect(() => {
    // Register the locale for country names (in English)
    countries.registerLocale(enLocale);

    // Fetch country names in English
    const countryNames = countries.getNames("en", { select: "official" });
    setCountryOptions(countryNames); // Save the country options in the state
  }, []);

  const handleCountryChange = (e) => {
    setSelectedCountry(e.target.value);
  };

  const handleAvatar = (e) => {
    if (e.target.files[0]) {
      setAvatar({
        file: e.target.files[0],
        url: URL.createObjectURL(e.target.files[0]),
      });
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData(e.target);
    const { username, email, password } = Object.fromEntries(formData);

    try {
      const res = await createUserWithEmailAndPassword(auth, email, password);
      const imgUrl = await upload(avatar.file);
      await setDoc(doc(db, "users", res.user.uid), {
        username,
        email,
        avatar: imgUrl,
        id: res.user.uid,
        country: selectedCountry, // Add selected country to Firestore
        blocked: [],
      });
      await setDoc(doc(db, "userchats", res.user.uid), {
        chats: [],
      });

      toast.success("Account created! You can login now!");
    } catch (error) {
      console.log(error);
      toast.error(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.target);
    const { email, password } = Object.fromEntries(formData);

    try {
      await signInWithEmailAndPassword(auth, email, password);
    } catch (error) {
      console.log(error);
      toast.error(error.message);
    } finally {
      setLoading(false);
    }

    toast.success("You are logged in!");
  };

  return (
    <div className='login'>
      {/* Conditionally render based on isRegistering state */}
      <div className='item'>
        {isRegistering ? (
          <>
            <h2>Create an Account</h2>
            <form onSubmit={handleRegister}>
              <label htmlFor='file'>
                <img src={avatar.url || "./avatar.png"} alt='' />
                Upload an image
              </label>
              <input
                type='file'
                id='file'
                style={{ display: "none" }}
                onChange={handleAvatar}
              />
              <input type='text' placeholder='Username' name='username' />
              <input type='text' placeholder='Email' name='email' />
              <input type='password' placeholder='Password' name='password' />

              {/* Country Select Dropdown */}
              <select
                name='country'
                value={selectedCountry}
                onChange={handleCountryChange}
                required>
                <option value='' disabled>
                  -- Select Your Country --
                </option>
                {Object.entries(countryOptions).map(
                  ([countryCode, countryName]) => (
                    <option key={countryCode} value={countryCode}>
                      {countryName}
                    </option>
                  )
                )}
              </select>

              <button disabled={loading}>
                {loading ? "Loading" : "Sign up"}
              </button>
            </form>
            <p>
              Already registered?{" "}
              <button
                type='button'
                onClick={() => setIsRegistering(false)}
                className='link-button'>
                Sign in here
              </button>
            </p>
          </>
        ) : (
          <>
            <h2>Welcome back</h2>
            <form onSubmit={handleLogin}>
              <input type='text' placeholder='Email' name='email' />
              <input type='password' placeholder='Password' name='password' />
              <button disabled={loading}>
                {loading ? "Loading" : "Sign in"}
              </button>
            </form>
            <p>
              Not registered?{" "}
              <button
                type='button'
                onClick={() => setIsRegistering(true)}
                className='link-button'>
                Sign up here
              </button>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
