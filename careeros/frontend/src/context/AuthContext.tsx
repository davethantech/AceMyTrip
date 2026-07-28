"use client";

import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { UserResponse } from "../types";
import { authService } from "../services";

interface AuthContextType {
  user: UserResponse | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, fullName: string, password: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  const refreshUser = useCallback(async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
    } catch {
      setUser(null);
    }
  }, []);

  useEffect(() => {
    const initAuth = async () => {
      if (authService.isAuthenticated()) {
        await refreshUser();
      }
      setIsLoading(false);
    };

    initAuth();

    // Listen for logout events
    const handleLogout = () => {
      setUser(null);
    };

    window.addEventListener("auth:logout", handleLogout);
    return () => window.removeEventListener("auth:logout", handleLogout);
  }, [refreshUser]);

  const login = async (email: string, password: string) => {
    try {
      await authService.login({ email, password });
      await refreshUser();
      router.push("/dashboard");
    } catch (error) {
      throw error;
    }
  };

  const register = async (email: string, fullName: string, password: string) => {
    try {
      await authService.register({ email, full_name: fullName, password });
      await login(email, password);
    } catch (error) {
      throw error;
    }
  };

  const logout = () => {
    authService.logout();
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        register,
        logout,
        refreshUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
