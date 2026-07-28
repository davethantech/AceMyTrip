'use client';

import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button } from '@/components/ui';
import { applicationsService } from '@/services/applications';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import type { ApplicationResponse, ApplicationStatus } from '@/types';

const statusColors: Record<ApplicationStatus, string> = {
  draft: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
  applied: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  interview: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  offer: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  rejected: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  withdrawn: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
};

export default function ApplicationsPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthContext();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [filterStatus, setFilterStatus] = useState<string>('all');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: applications = [], isLoading } = useQuery({
    queryKey: ['applications'],
    queryFn: () => applicationsService.getApplications(),
    enabled: isAuthenticated,
  });

  const deleteApplicationMutation = useMutation({
    mutationFn: (appId: string) => applicationsService.deleteApplication(appId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
    },
  });

  const handleDelete = (appId: string) => {
    if (confirm('Are you sure you want to delete this application?')) {
      deleteApplicationMutation.mutate(appId);
    }
  };

  const filteredApplications = filterStatus === 'all'
    ? applications
    : applications.filter((app: ApplicationResponse) => app.status === filterStatus);

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
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">My Applications</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Track and manage all your job applications.
          </p>
        </div>

        {/* Filter */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex gap-2 flex-wrap">
              <Button
                variant={filterStatus === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('all')}
              >
                All ({applications.length})
              </Button>
              {(['draft', 'applied', 'interview', 'offer', 'rejected', 'withdrawn'] as ApplicationStatus[]).map((status) => {
                const count = applications.filter((a: ApplicationResponse) => a.status === status).length;
                return (
                  <Button
                    key={status}
                    variant={filterStatus === status ? 'default' : 'outline'}
                    size="sm"
                    onClick={() => setFilterStatus(status)}
                  >
                    {status.charAt(0).toUpperCase() + status.slice(1)} ({count})
                  </Button>
                );
              })}
            </div>
          </CardContent>
        </Card>

        {/* Applications List */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : filteredApplications.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                No applications found.{' '}
                <Link href="/jobs" className="text-blue-600 hover:underline">
                  Search for jobs
                </Link>
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredApplications.map((app: ApplicationResponse) => (
              <Card key={app.id}>
                <CardContent className="pt-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                          Application #{app.id.slice(0, 8)}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[app.status]}`}>
                          {app.status.toUpperCase()}
                        </span>
                      </div>
                      {app.notes && (
                        <p className="text-gray-600 dark:text-gray-400 mt-2">{app.notes}</p>
                      )}
                      <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                        Created: {new Date(app.created_at).toLocaleDateString()}
                        {app.applied_date && ` • Applied: ${new Date(app.applied_date).toLocaleDateString()}`}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      <Link href={`/applications/${app.id}`}>
                        <Button variant="outline" size="sm">View Details</Button>
                      </Link>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(app.id)}
                        disabled={deleteApplicationMutation.isPending}
                      >
                        Delete
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
