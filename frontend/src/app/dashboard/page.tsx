'use client';

import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui';
import { applicationsService } from '@/services/applications';
import { jobsService } from '@/services/jobs';
import { resumesService } from '@/services/resumes';
import { useQuery } from '@tanstack/react-query';
import Link from 'next/link';
import type { ApplicationResponse } from '@/types';

export default function DashboardPage() {
  const { user, logout, isAuthenticated, isLoading: authLoading } = useAuthContext();
  const router = useRouter();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: applications = [] } = useQuery({
    queryKey: ['applications'],
    queryFn: () => applicationsService.getApplications(),
    enabled: isAuthenticated,
  });

  const { data: resumes = [] } = useQuery({
    queryKey: ['resumes'],
    queryFn: () => resumesService.getResumes(),
    enabled: isAuthenticated,
  });

  if (authLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  const stats = {
    totalApplications: applications.length,
    interviews: applications.filter((a: ApplicationResponse) => a.status === 'interview').length,
    offers: applications.filter((a: ApplicationResponse) => a.status === 'offer').length,
    resumes: resumes.length,
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow">
        <div className="container mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-blue-600 dark:text-blue-400">CareerOS</h1>
            <div className="flex items-center gap-4">
              <span className="text-gray-600 dark:text-gray-300">
                {user?.full_name}
              </span>
              <button
                onClick={() => logout()}
                className="text-sm text-red-600 hover:underline"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
            Welcome back, {user?.full_name}!
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Here&apos;s an overview of your job search progress.
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Total Applications
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.totalApplications}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Interviews
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-green-600">{stats.interviews}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Offers
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-blue-600">{stats.offers}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Resumes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">
                {stats.resumes}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link href="/jobs">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle>Search Jobs</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 dark:text-gray-400">
                  Find new job opportunities matching your preferences.
                </p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/applications">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle>Track Applications</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 dark:text-gray-400">
                  Manage and track all your job applications.
                </p>
              </CardContent>
            </Card>
          </Link>

          <Link href="/resumes">
            <Card className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardHeader>
                <CardTitle>Manage Resumes</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600 dark:text-gray-400">
                  Create and optimize your resumes with AI.
                </p>
              </CardContent>
            </Card>
          </Link>
        </div>

        {/* Recent Applications */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Applications</CardTitle>
          </CardHeader>
          <CardContent>
            {applications.length === 0 ? (
              <p className="text-gray-600 dark:text-gray-400">
                No applications yet. Start by searching for jobs!
              </p>
            ) : (
              <div className="space-y-4">
                {applications.slice(0, 5).map((app: ApplicationResponse) => (
                  <div
                    key={app.id}
                    className="flex justify-between items-center p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        Application #{app.id.slice(0, 8)}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Status: {app.status}
                      </p>
                    </div>
                    <Link href={`/applications/${app.id}`}>
                      <button className="text-blue-600 hover:underline text-sm">
                        View Details
                      </button>
                    </Link>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
