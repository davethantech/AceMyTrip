'use client';

import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from '@/components/ui';
import { usersService } from '@/services/users';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import { useForm } from 'react-hook-form';
import type { UserUpdate, UserResponse } from '@/types';

export default function ProfilePage() {
  const { user: authUser, isAuthenticated, isLoading: authLoading, logout } = useAuthContext();
  const router = useRouter();
  const queryClient = useQueryClient();

  const { register, handleSubmit, formState: { errors } } = useForm<UserUpdate>();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: userProfile, isLoading } = useQuery({
    queryKey: ['userProfile'],
    queryFn: () => usersService.getCurrentUser(),
    enabled: isAuthenticated,
  });

  const updateProfileMutation = useMutation({
    mutationFn: (data: UserUpdate) => usersService.updateCurrentUser(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['userProfile', 'currentUser'] });
      alert('Profile updated successfully!');
    },
    onError: (error) => {
      console.error('Failed to update profile:', error);
      alert('Failed to update profile. Please try again.');
    },
  });

  const onSubmit = (data: UserUpdate) => {
    updateProfileMutation.mutate(data);
  };

  if (authLoading || isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const user = userProfile || authUser;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <Link href="/dashboard">
              <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">CareerOS</h1>
            </Link>
            <Link href="/dashboard" className="text-sm text-gray-600 dark:text-gray-400 hover:underline">
              ← Back to Dashboard
            </Link>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">My Profile</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Manage your account settings and preferences.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {/* Profile Information */}
          <Card>
            <CardHeader>
              <CardTitle>Account Information</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <label className="text-sm text-gray-600 dark:text-gray-400">Full Name</label>
                  <p className="text-lg font-medium text-gray-900 dark:text-white">
                    {user?.full_name}
                  </p>
                </div>
                <div>
                  <label className="text-sm text-gray-600 dark:text-gray-400">Email</label>
                  <p className="text-lg font-medium text-gray-900 dark:text-white">
                    {user?.email}
                  </p>
                </div>
                <div>
                  <label className="text-sm text-gray-600 dark:text-gray-400">Role</label>
                  <p className="text-lg font-medium text-gray-900 dark:text-white capitalize">
                    {user?.role}
                  </p>
                </div>
                <div>
                  <label className="text-sm text-gray-600 dark:text-gray-400">Member Since</label>
                  <p className="text-lg font-medium text-gray-900 dark:text-white">
                    {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Edit Profile Form */}
          <Card>
            <CardHeader>
              <CardTitle>Edit Profile</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div>
                  <label htmlFor="full_name" className="block text-sm font-medium mb-1">
                    Full Name
                  </label>
                  <Input
                    id="full_name"
                    type="text"
                    defaultValue={user?.full_name}
                    {...register('full_name')}
                  />
                </div>
                <div>
                  <label htmlFor="email" className="block text-sm font-medium mb-1">
                    Email
                  </label>
                  <Input
                    id="email"
                    type="email"
                    defaultValue={user?.email}
                    {...register('email')}
                  />
                </div>
                <Button 
                  type="submit" 
                  className="w-full"
                  disabled={updateProfileMutation.isPending}
                >
                  {updateProfileMutation.isPending ? 'Updating...' : 'Update Profile'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>

        {/* Account Actions */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Account Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex gap-4">
              <Button
                variant="outline"
                onClick={() => router.push('/settings')}
              >
                Settings
              </Button>
              <Button
                variant="destructive"
                onClick={() => logout()}
              >
                Logout
              </Button>
            </div>
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
