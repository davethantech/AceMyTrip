"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { User } from "lucide-react";

export default function ProfilePage() {
  const router = useRouter();
  const { user, isAuthenticated, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, isLoading, router]);

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        My Profile
      </h1>
      
      <div className="max-w-2xl bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-20 h-20 rounded-full bg-primary flex items-center justify-center text-primary-foreground text-2xl font-bold">
            {user.full_name.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">
              {user.full_name}
            </h2>
            <p className="text-gray-600 dark:text-gray-400">{user.email}</p>
            <span className="inline-block mt-1 px-2 py-1 bg-primary/10 text-primary text-xs rounded capitalize">
              {user.role}
            </span>
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-gray-700 pt-6 space-y-4">
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">Account Status</label>
            <p className="font-medium text-gray-900 dark:text-white">
              {user.is_verified ? "Verified" : "Pending Verification"}
            </p>
          </div>
          <div>
            <label className="text-sm text-gray-600 dark:text-gray-400">Member Since</label>
            <p className="font-medium text-gray-900 dark:text-white">
              {new Date(user.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
