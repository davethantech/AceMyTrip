"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useQuery } from "@tanstack/react-query";
import { applicationService, jobService, resumeService } from "@/services";
import {
  Briefcase,
  FileText,
  CheckCircle,
  TrendingUp,
  Calendar,
  Target,
} from "lucide-react";
import { ApplicationStatus } from "@/types";

export default function DashboardPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  const { data: applications = [] } = useQuery({
    queryKey: ["applications"],
    queryFn: () => applicationService.getApplications(),
    enabled: !!user,
  });

  const { data: jobs = [] } = useQuery({
    queryKey: ["jobs"],
    queryFn: () => jobService.searchJobs({ limit: 10 }),
    enabled: !!user,
  });

  const { data: resumes = [] } = useQuery({
    queryKey: ["resumes"],
    queryFn: () => resumeService.getResumes(),
    enabled: !!user,
  });

  if (authLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  const stats = [
    {
      name: "Total Applications",
      value: applications.length,
      icon: Briefcase,
      change: "+12% from last month",
    },
    {
      name: "Interviews",
      value: applications.filter(
        (a) => a.status === ApplicationStatus.INTERVIEW
      ).length,
      icon: Calendar,
      change: "This week",
    },
    {
      name: "Resumes",
      value: resumes.length,
      icon: FileText,
      change: `${resumes.filter((r) => r.is_primary).length} primary`,
    },
    {
      name: "Avg ATS Score",
      value:
        resumes.length > 0
          ? Math.round(
              resumes.reduce((acc, r) => acc + (r.ats_score || 0), 0) /
                resumes.length
            )
          : 0,
      icon: Target,
      change: "Out of 100",
    },
  ];

  const statusCounts = Object.values(ApplicationStatus).reduce(
    (acc, status) => {
      acc[status] = applications.filter((a) => a.status === status).length;
      return acc;
    },
    {} as Record<ApplicationStatus, number>
  );

  return (
    <div className="p-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
          Welcome back, {user.full_name}!
        </h1>
        <p className="mt-2 text-gray-600 dark:text-gray-400">
          Here&apos;s an overview of your job search progress.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6"
          >
            <div className="flex items-center">
              <div className="flex-shrink-0 bg-primary/10 rounded-lg p-3">
                <stat.icon className="w-6 h-6 text-primary" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                  {stat.name}
                </p>
                <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                  {stat.value}
                </p>
              </div>
            </div>
            <div className="mt-4 flex items-center text-sm">
              <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-gray-500 dark:text-gray-400">
                {stat.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Application Status Breakdown */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Applications by Status
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {Object.entries(statusCounts).map(([status, count]) => (
            <div
              key={status}
              className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
            >
              <p className="text-2xl font-bold text-primary">{count}</p>
              <p className="text-xs text-gray-600 dark:text-gray-400 capitalize mt-1">
                {status}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Applications */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Recent Applications
        </h2>
        {applications.length === 0 ? (
          <div className="text-center py-8">
            <CheckCircle className="w-12 h-12 text-gray-400 mx-auto mb-3" />
            <p className="text-gray-600 dark:text-gray-400">
              No applications yet. Start applying to jobs!
            </p>
            <button
              onClick={() => router.push("/jobs")}
              className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
            >
              Browse Jobs
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {applications.slice(0, 5).map((application) => (
              <div
                key={application.id}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700 rounded-lg"
              >
                <div>
                  <p className="font-medium text-gray-900 dark:text-white">
                    Job ID: {application.job_id.slice(0, 8)}...
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Applied:{" "}
                    {new Date(application.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span
                  className={`px-3 py-1 text-xs font-medium rounded-full capitalize ${
                    application.status === ApplicationStatus.INTERVIEW
                      ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                      : application.status === ApplicationStatus.OFFER
                      ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                      : application.status === ApplicationStatus.REJECTED
                      ? "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200"
                      : "bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-200"
                  }`}
                >
                  {application.status}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
