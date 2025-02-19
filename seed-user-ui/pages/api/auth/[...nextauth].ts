import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import axios from "axios";

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        try {
          console.log("🟡 Sending request to FastAPI:", credentials);

          const res = await axios.post(
            "http://localhost:8000/auth/login",
            JSON.stringify({ email: credentials?.email, password: credentials?.password }), // Ensure JSON format
            { headers: { "Content-Type": "application/json" } } // Set proper headers
          );

          console.log("✅ FastAPI Response:", res.data);
          return res.data;
        } catch (error) {
          console.error("❌ FastAPI Login Error:", error.response?.data || error.message);
          return null;
        }
      },
    }),
  ],
  session: { strategy: "jwt" },
  secret: process.env.NEXTAUTH_SECRET,
});
