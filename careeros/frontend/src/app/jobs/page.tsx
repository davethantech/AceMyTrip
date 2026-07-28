"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { jobService, applicationService } from "@/services";
import { aiService } from "@/services/ai";
import { Briefcase, MapPin, DollarSign, Search, Filter, ExternalLink } from "lucide-react";
import type { JobResponse, RemoteType, JobType } from "@/types";

export default function JobsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedJob, setSelectedJob] = useState<JobResponse | null>(null);
  const [filters, setFilters] = useState<{
    remote_type?: RemoteType;
    job_type?: JobType;
    location?: string;
  }>({});

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: jobs = [], isLoading } = useQuery({
    queryKey: ["jobs", searchQuery, filters],
    queryFn: () =>
      jobService.searchJobs({
        query: searchQuery || undefined,
        ...filters,
        limit: 50,
      }),
    enabled: !!user,
  });

  const applyMutation = useMutation({
    mutationFn: (jobId: string) =>
      applicationService.createApplication({ job_id: jobId }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
      alert("Application submitted successfully!");
    },
    onError: (error: Error) => {
      alert(`Failed to apply: ${error.message}`);
    },
  });

  const handleApply = (job: JobResponse) => {
    if (window.confirm(`Apply for ${job.title}?`)) {
      applyMutation.mutate(job.id);
    }
  };

  const handleJobMatch = async (job: JobResponse) => {
    // This would require a resume to be selected
    alert("Job matching requires a resume. Please upload your resume first.");
    router.push("/resumes");
  };

  if (authLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Job Search
        </h1>

        {/* Search Bar */}
        <div className="flex gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search jobs by title, company, or keywords..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
          </div>
          <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors flex items-center gap-2">
            <Filter className="w-5 h-5" />
            Filters
          </button>
        </div>

        {/* Quick Filters */}
        <div className="flex gap-2 flex-wrap">
          {["remote", "hybrid", "onsite"].map((type) => (
            <button
              key={type}
              onClick={() =>
                setFilters((prev) => ({
                  ...prev,
                  remote_type: prev.remote_type === type ? undefined : (type as RemoteType),
                }))
              }
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                filters.remote_type === type
                  ? "bg-primary text-primary-foreground"
                  : "bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600"
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Jobs Grid */}
      {isLoading ? (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 animate-pulse"
            >
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mb-4"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-2"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
            </div>
          ))}
        </div>
      ) : jobs.length === 0 ? (
        <div className="text-center py-12">
          <Briefcase className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No jobs found
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Try adjusting your search or filters
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {jobs.map((job) => (
            <div
              key={job.id}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {job.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400">
                    Company ID: {job.company_id.slice(0, 8)}...
                  </p>
                </div>
                <a
                  href={job.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-primary hover:text-primary/80"
                >
                  <ExternalLink className="w-5 h-5" />
                </a>
              </div>

              <div className="space-y-2 mb-4">
                {job.location && (
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <MapPin className="w-4 h-4 mr-2" />
                    {job.location}
                  </div>
                )}
                {job.salary_min && job.salary_max && (
                  <div className="flex items-center text-sm text-gray-600 dark:text-gray-400">
                    <DollarSign className="w-4 h-4 mr-2" />
                    ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}{" "}
                    {job.currency}
                  </div>
                )}
                <div className="flex gap-2">
                  <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs rounded capitalize">
                    {job.remote_type}
                  </span>
                  <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs rounded capitalize">
                    {job.job_type}
                  </span>
                </div>
              </div>

              {job.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-3 mb-4">
                  {job.description}
                </p>
              )}

              <div className="flex gap-2">
                <button
                  onClick={() => handleApply(job)}
                  disabled={applyMutation.isPending}
                  className="flex-1 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors text-sm font-medium disabled:opacity-50"
                >
                  {applyMutation.isPending ? "Applying..." : "Apply Now"}
                </button>
                <button
                  onClick={() => handleJobMatch(job)}
                  className="flex-1 px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors text-sm font-medium"
                >
                  Match Resume
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
