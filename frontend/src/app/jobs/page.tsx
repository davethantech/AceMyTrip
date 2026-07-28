'use client';

import { useAuthContext } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from '@/components/ui';
import { jobsService } from '@/services/jobs';
import { applicationsService } from '@/services/applications';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Link from 'next/link';
import type { JobResponse, RemoteType, JobType, ApplicationCreate } from '@/types';

export default function JobsPage() {
  const { isAuthenticated, isLoading: authLoading } = useAuthContext();
  const router = useRouter();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');
  const [remoteType, setRemoteType] = useState<string>('');
  const [jobType, setJobType] = useState<string>('');

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: jobs = [], isLoading } = useQuery({
    queryKey: ['jobs', searchQuery, remoteType, jobType],
    queryFn: () => jobsService.searchJobs({
      query: searchQuery || undefined,
      remote_type: remoteType || undefined,
      job_type: jobType || undefined,
      skip: 0,
      limit: 50,
    }),
    enabled: isAuthenticated,
  });

  const createApplicationMutation = useMutation({
    mutationFn: (data: ApplicationCreate) => applicationsService.createApplication(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] });
      alert('Application created successfully!');
    },
    onError: (error) => {
      console.error('Failed to create application:', error);
      alert('Failed to create application. Please try again.');
    },
  });

  const handleApply = (jobId: string) => {
    createApplicationMutation.mutate({
      job_id: jobId,
      status: 'draft',
    });
  };

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
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Search Jobs</h2>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Find job opportunities matching your preferences.
          </p>
        </div>

        {/* Filters */}
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Input
                placeholder="Search by title or keywords..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <select
                value={remoteType}
                onChange={(e) => setRemoteType(e.target.value)}
                className="px-3 py-2 border rounded-md dark:bg-gray-800 dark:border-gray-700"
              >
                <option value="">All Remote Types</option>
                <option value="remote">Remote</option>
                <option value="hybrid">Hybrid</option>
                <option value="onsite">Onsite</option>
              </select>
              <select
                value={jobType}
                onChange={(e) => setJobType(e.target.value)}
                className="px-3 py-2 border rounded-md dark:bg-gray-800 dark:border-gray-700"
              >
                <option value="">All Job Types</option>
                <option value="full_time">Full Time</option>
                <option value="part_time">Part Time</option>
                <option value="contract">Contract</option>
                <option value="freelance">Freelance</option>
                <option value="internship">Internship</option>
              </select>
              <Button onClick={() => queryClient.invalidateQueries({ queryKey: ['jobs'] })}>
                Search
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Jobs List */}
        {isLoading ? (
          <div className="flex justify-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
          </div>
        ) : jobs.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                No jobs found. Try adjusting your search filters.
              </p>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {jobs.map((job: JobResponse) => (
              <Card key={job.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="pt-6">
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                        {job.title}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400 mt-1">
                        {job.location || 'Remote'} • {job.remote_type} • {job.job_type}
                      </p>
                      {job.salary_min && job.salary_max && (
                        <p className="text-green-600 dark:text-green-400 mt-1">
                          ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()} {job.currency}
                        </p>
                      )}
                      {job.description && (
                        <p className="text-gray-600 dark:text-gray-400 mt-3 line-clamp-2">
                          {job.description}
                        </p>
                      )}
                      {job.skills && job.skills.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3">
                          {job.skills.slice(0, 5).map((skill: string, index: number) => (
                            <span
                              key={index}
                              className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    <div className="flex flex-col gap-2 ml-4">
                      <Link href={job.url} target="_blank" rel="noopener noreferrer">
                        <Button variant="outline" size="sm">View Details</Button>
                      </Link>
                      <Button
                        size="sm"
                        onClick={() => handleApply(job.id)}
                        disabled={createApplicationMutation.isPending}
                      >
                        {createApplicationMutation.isPending ? 'Applying...' : 'Apply Now'}
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
