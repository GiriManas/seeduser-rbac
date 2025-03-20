<div className="grid grid-cols-1 md:grid-cols-3 gap-6">
  {DISPLAY_APPS.map((item) => (
    <Link href={item.link} key={item.id} className="w-full">
      <Card className="w-[280px] h-[150px] shadow-md transition-transform hover:scale-105 cursor-pointer flex flex-col justify-center">
        <CardHeader>
          <CardTitle className="text-lg">{item.name}</CardTitle>
          <CardDescription className="text-sm">{item.description}</CardDescription>
        </CardHeader>
      </Card>
    </Link>
  ))}
</div>