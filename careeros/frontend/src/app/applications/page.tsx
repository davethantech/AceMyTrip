"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { applicationService } from "@/services";
import { CheckSquare, Calendar, FileText, User, Trash2, Edit } from "lucide-react";
import type { ApplicationStatus } from "@/types";

export default function ApplicationsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user, isAuthenticated, isLoading: authLoading } = useAuth();
  const [selectedStatus, setSelectedStatus] = useState<ApplicationStatus | "all">("all");

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [isAuthenticated, authLoading, router]);

  const { data: applications = [], isLoading } = useQuery({
    queryKey: ["applications"],
    queryFn: () => applicationService.getApplications(),
    enabled: !!user,
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => applicationService.deleteApplication(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["applications"] });
    },
  });

  const handleDelete = (id: string) => {
    if (window.confirm("Are you sure you want to delete this application?")) {
      deleteMutation.mutate(id);
    }
  };

  const filteredApplications =
    selectedStatus === "all"
      ? applications
      : applications.filter((a) => a.status === selectedStatus);

  const statusCounts = Object.values(ApplicationStatus).reduce(
    (acc, status) => {
      acc[status] = applications.filter((a) => a.status === status).length;
      return acc;
    },
    {} as Record<ApplicationStatus, number>
  );

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
          Applications Tracker
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Track and manage all your job applications in one place.
        </p>
      </div>

      {/* Status Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        <button
          onClick={() => setSelectedStatus("all")}
          className={`p-4 rounded-xl border transition-colors ${
            selectedStatus === "all"
              ? "bg-primary text-primary-foreground border-primary"
              : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
          }`}
        >
          <p className="text-2xl font-bold">{applications.length}</p>
          <p className="text-sm opacity-80">All</p>
        </button>
        {Object.values(ApplicationStatus).map((status) => (
          <button
            key={status}
            onClick={() => setSelectedStatus(status)}
            className={`p-4 rounded-xl border transition-colors ${
              selectedStatus === status
                ? "bg-primary text-primary-foreground border-primary"
                : "bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700"
            }`}
          >
            <p className="text-2xl font-bold">{statusCounts[status]}</p>
            <p className="text-sm opacity-80 capitalize">{status}</p>
          </button>
        ))}
      </div>

      {/* Applications List */}
      {isLoading ? (
        <div className="space-y-4">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700 animate-pulse"
            >
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
            </div>
          ))}
        </div>
      ) : filteredApplications.length === 0 ? (
        <div className="text-center py-12 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700">
          <CheckSquare className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
            No applications found
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            Start applying to jobs to track your applications here.
          </p>
          <button
            onClick={() => router.push("/jobs")}
            className="px-6 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition-colors"
          >
            Browse Jobs
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredApplications.map((application) => (
            <div
              key={application.id}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-700"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
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
                    <span className="text-sm text-gray-500 dark:text-gray-400">
                      Applied: {new Date(application.created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Job ID: {application.job_id}
                  </p>
                  {application.notes && (
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                      Notes: {application.notes}
                    </p>
                  )}
                  {application.follow_up_date && (
                    <div className="mt-2 flex items-center text-sm text-gray-600 dark:text-gray-400">
                      <Calendar className="w-4 h-4 mr-2" />
                      Follow-up: {new Date(application.follow_up_date).toLocaleDateString()}
                    </div>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => router.push(`/applications/${application.id}`)}
                    className="p-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                    title="View details"
                  >
                    <FileText className="w-5 h-5" />
                  </button>
                  <button
                    onClick={() => handleDelete(application.id)}
                    disabled={deleteMutation.isPending}
                    className="p-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors disabled:opacity-50"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
